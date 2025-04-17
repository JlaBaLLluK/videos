from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.settings import api_settings
from rest_framework.status import HTTP_200_OK

from .authentication import JwtAuthenticationNoException
from . import models
from . import serializers
from . import permissions
from . import mixins


class ModelViewSet(
    mixins.ActionsSerializersMapMixin,
    mixins.ActionsPermissionsMapMixin,
    viewsets.ModelViewSet,
):
    pass


@extend_schema_view(
    list=extend_schema(description="List or users"),
    create=extend_schema(description="Create new user"),
    retrieve=extend_schema(description="Get single user by id"),
    update=extend_schema(description="User update"),
    partial_update=extend_schema(description="Partial user update"),
    destroy=extend_schema(description="User delete"),
)
@extend_schema(tags=["User"])
class UserViewSet(mixins.CreateObjectWithIdInFilePathMixin, ModelViewSet):
    queryset = models.User.objects.filter()
    serializer_class = serializers.UserListSerializer
    actions_serializers_map = {
        "list": serializer_class,
        "create": serializers.UserCreateSerializer,
        "retrieve": serializers.UserDetailSerializer,
        "update": serializers.UserUpdateSerializer,
        "partial_update": serializers.UserUpdateSerializer,
        "me": serializers.UserDetailSerializer,
        "update_password": serializers.UpdatePasswordSerializer,
        "subscribers": serializer_class,
        "subscriptions": serializer_class,
    }
    permission_classes = [
        permissions.IsUserItself,
        IsAuthenticatedOrReadOnly,
    ]
    actions_permissions_map = {
        "create": [],
        "subscribe": [IsAuthenticated],
        "subscribers": [IsAuthenticated],
        "subscriptions": [IsAuthenticated],
    }
    file_fields_and_functions = {"profile_photo": models.profile_photo_upload_to}
    lookup_field = "username"

    def get_authenticators(self):
        if self.request.method in ["PATCH", "PUT"]:
            self.authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES
        elif self.request.method == "GET":
            self.authentication_classes = [JwtAuthenticationNoException]

        return super().get_authenticators()

    def perform_update(self, serializer):
        instance = self.get_object()
        instance.profile_photo.delete(save=False)
        super().perform_update(serializer)

    @extend_schema(description="Update user password")
    @action(
        methods=["PATCH"],
        detail=False,
        url_path="update-password",
    )
    def update_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success": "Password updated successfully"})

    @extend_schema(description="Get authenticated user data")
    @action(
        methods=["GET"],
        detail=False,
        authentication_classes=api_settings.DEFAULT_AUTHENTICATION_CLASSES,
    )
    def me(self, request):
        serializer = self.get_serializer(instance=request.user)
        return Response(serializer.data)

    @action(methods=["PUT"], detail=True)
    def subscribe(self, request, *args, **kwargs):
        target_user = self.get_object()
        if request.user in target_user.subscribers.all():
            target_user.subscribers.remove(request.user)
            is_request_user_subscribed = False
        else:
            target_user.subscribers.add(request.user)
            is_request_user_subscribed = True

        return Response(
            {
                "subscribers_count": target_user.subscribers_count,
                "is_request_user_subscribed": is_request_user_subscribed,
            },
            HTTP_200_OK,
        )

    @action(
        methods=["GET"],
        detail=False,
        authentication_classes=api_settings.DEFAULT_AUTHENTICATION_CLASSES,
    )
    def subscribers(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=request.user.subscribers, many=True)
        return Response(serializer.data, HTTP_200_OK)

    @action(
        methods=["GET"],
        detail=False,
        authentication_classes=api_settings.DEFAULT_AUTHENTICATION_CLASSES,
    )
    def subscriptions(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=request.user.subscriptions, many=True)
        return Response(serializer.data, HTTP_200_OK)
