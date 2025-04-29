from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.settings import api_settings
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from .authentication import JwtAuthenticationNoException
from . import models
from . import serializers
from . import permissions
from . import mixins

from apps.video import models as video_models
from apps.playlist import models as playlist_models
from apps.video import serializers as video_serializers
from apps.playlist import serializers as playlist_serializers


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
class UserViewSet(ModelViewSet):
    queryset = models.User.objects.filter()
    serializer_class = serializers.UserListSerializer
    actions_serializers_map = {
        "list": serializer_class,
        "create": serializers.UserCreateSerializer,
        "retrieve": serializers.UserDetailSerializer,
        "update": serializers.UserUpdateSerializer,
        "partial_update": serializers.UserUpdateSerializer,
        "destroy": serializers.UserDeleteSerializer,
        "registration_confirm": serializers.UserRegistrationConfirmSerializer,
        "me": serializers.UserDetailSerializer,
        "update_password": serializers.UpdatePasswordSerializer,
        "subscribers": serializer_class,
        "subscriptions": serializer_class,
        "send_reset_password_code": serializers.ResetPasswordCodeSerializer,
        "reset_password": serializers.SendPasswordSerializer,
    }
    permission_classes = [
        permissions.IsUserItself,
        IsAuthenticatedOrReadOnly,
    ]
    actions_permissions_map = {
        "create": [],
        "registration_confirm": [],
        "send_reset_password_code": [],
        "reset_password": [],
        "subscribe": [IsAuthenticated],
        "subscribers": [IsAuthenticated],
        "subscriptions": [IsAuthenticated],
    }
    authentication_classes = []
    lookup_field = "username"

    def get_authenticators(self):
        act = self.request.resolver_match.view_name
        if act == "user-registration-confirm":
            self.authentication_classes = []
        elif act == "user-reset-password":
            self.authentication_classes = []
        elif self.request.method in ["PUT", "PATCH"]:
            self.authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES
        elif self.request.method == "GET":
            self.authentication_classes = [JwtAuthenticationNoException]
        elif self.request.method == "DELETE":
            self.authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES

        return super().get_authenticators()

    @action(methods=["PATCH"], detail=False, url_path="registration-confirm")
    def registration_confirm(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Регистрация завершена успешно."}, HTTP_200_OK)

    def perform_update(self, serializer):
        instance = self.get_object()
        instance.profile_photo.delete(save=False)
        super().perform_update(serializer)

    def destroy(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data={"password": request.query_params.get("password")}
        )
        serializer.is_valid(raise_exception=True)
        return super().destroy(request, *args, **kwargs)

    @action(methods=["GET"], detail=True, url_path="send-reset-password-code")
    def send_reset_password_code(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance)
        code = serializer.save()
        return Response({"code": code}, HTTP_200_OK)

    @action(methods=["PATCH"], detail=True, url_path="reset-password")
    def reset_password(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance)
        serializer.save()
        return Response()

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


class SearchView(APIView):
    authentication_classes = []

    def get(self, request):
        query = request.query_params.get("search_query")
        if not query:
            return Response()

        videos = video_models.Video.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        users = models.User.objects.filter(
            Q(username__icontains=query)
            | Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
        )
        playlists = playlist_models.Playlist.objects.filter(Q(name__icontains=query))
        video_serializer = video_serializers.VideosListSerializer(videos, many=True)
        users_serializer = serializers.UserListSerializer(
            users, many=True, context={"request": request}
        )
        playlist_serializer = playlist_serializers.PlaylistsListSerializer(
            playlists, many=True, context={"request": request}
        )
        content_type = request.query_params.get("content_type")
        response_data = {
            "videos": video_serializer.data,
            "channels": users_serializer.data,
            "playlists": playlist_serializer.data,
        }
        return Response(response_data[content_type] if content_type else response_data)
