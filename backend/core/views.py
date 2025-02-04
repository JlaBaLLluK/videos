from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from drf_spectacular.utils import extend_schema_view, extend_schema

from core import models as core_models
from core import serializers as core_serializers
from core import permissions as core_permissions

@extend_schema_view(
    list=extend_schema(
        description="List or users"
    ),
    create=extend_schema(
        description="Create new user"
    ),
    retreive=extend_schema(
        description="Get single user by id"
    ),
    update=extend_schema(
        description="User update"
    ),
    partial_update=extend_schema(
        description="Partial user update"
    ),
    destroy=extend_schema(
        description="User delete"
    )
)
@extend_schema(
    tags=["User",]
)
class UserViewSet(viewsets.ModelViewSet):
    queryset = core_models.User.objects.filter(is_active=True)
    serializer_class = core_serializers.UserSerializer
    permission_classes = [core_permissions.IsUserItself, IsAuthenticated, ]

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = []

        return super().get_permissions()

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.is_active = False
        obj.save()
        return Response(self.serializer_class(instance=obj).data, status=HTTP_200_OK)
