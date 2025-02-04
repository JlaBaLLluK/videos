from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter

from core import models as core_models
from core import serializers as core_serializers
from core import permissions as core_permissions


@extend_schema_view(
    list=extend_schema(description="List or users"),
    create=extend_schema(description="Create new user"),
    retreive=extend_schema(description="Get single user by id"),
    update=extend_schema(description="User update"),
    partial_update=extend_schema(description="Partial user update"),
    destroy=extend_schema(description="User delete"),
)
@extend_schema(
    tags=[
        "User",
    ]
)
class UserViewSet(viewsets.ModelViewSet):
    queryset = core_models.User.objects.filter()
    serializer_class = core_serializers.UserSerializer
    permission_classes = [
        core_permissions.IsUserItself,
        IsAuthenticated,
    ]

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = []

        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ["update", "partial_update"]:
            self.serializer_class = core_serializers.UserDetailSerializer

        return super().get_serializer_class()

    @extend_schema(
        description="Update user password",
        parameters=[
            OpenApiParameter(
                name="id",
                description="A unique integer value identifying this user.",
                location=OpenApiParameter.PATH,
                required=True,
                type=int
            )
        ],
        request=core_serializers.UpdatePasswordSerializer,
    )
    @action(methods=["PATCH",], detail=True, url_path="change-password", serializer_class=core_serializers.UpdatePasswordSerializer)
    def change_password(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.get_object()
        user.set_password(serializer.validated_data["new_password"])
        user.save()
        return Response({"success": "Password updated successfully"})
