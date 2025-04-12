from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema_view, extend_schema

from core import models as core_models
from core import serializers as core_serializers
from core import permissions as core_permissions
from core import mixins as core_mixins


@extend_schema_view(
    list=extend_schema(description="List or users"),
    create=extend_schema(description="Create new user"),
    retrieve=extend_schema(description="Get single user by id"),
    update=extend_schema(description="User update"),
    partial_update=extend_schema(description="Partial user update"),
    destroy=extend_schema(description="User delete"),
)
@extend_schema(tags=["User"])
class UserViewSet(core_mixins.CreateObjectWithIdInFilePathMixin, viewsets.ModelViewSet):
    queryset = core_models.User.objects.filter()
    serializer_class = core_serializers.UserCreateSerializer
    permission_classes = [
        core_permissions.IsUserItself,
        IsAuthenticatedOrReadOnly,
    ]
    file_fields_and_functions = {"profile_photo": core_models.profile_photo_upload_to}
    lookup_field = "username"

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = []

        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ["update", "partial_update"]:
            self.serializer_class = core_serializers.UserUpdateSerializer
        elif self.action == "retrieve":
            self.serializer_class = core_serializers.UserDetailSerializer

        return super().get_serializer_class()

    def perform_update(self, serializer):
        instance = self.get_object()
        instance.profile_photo.delete(save=False)
        super().perform_update(serializer)

    @extend_schema(
        description="Update user password",
    )
    @action(
        methods=["PATCH"],
        detail=True,
        url_path="update-password",
        serializer_class=core_serializers.UpdatePasswordSerializer,
    )
    def update_password(self, request, username=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success": "Password updated successfully"})

    @extend_schema(description="Get authenticated user data")
    @action(
        methods=["GET"],
        detail=False,
        serializer_class=core_serializers.UserDetailSerializer,
    )
    def me(self, request):
        serializer = self.get_serializer(instance=request.user)
        return Response(serializer.data)
