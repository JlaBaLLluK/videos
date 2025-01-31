from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from core import models as core_models
from core import serializers as core_serializers
from core import permissions as core_permissions


class UserViewSet(viewsets.ModelViewSet):
    queryset = core_models.User.objects.filter(is_active=True)
    serializer_class = core_serializers.UserSerializer
    permission_classes = [core_permissions.IsUserItself, IsAuthenticated, ]

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.is_active = False
        obj.save()
        return Response(self.serializer_class(instance=obj).data, status=HTTP_200_OK)
