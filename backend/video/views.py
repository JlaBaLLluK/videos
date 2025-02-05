from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from core import permissions as core_permissions
from video import serializers as video_serializers
from video import models as video_models


@extend_schema_view(
    list=extend_schema(description="List or videos"),
    create=extend_schema(description="Upload new video"),
    retrieve=extend_schema(description="Get single video by id"),
    update=extend_schema(description="Video update"),
    partial_update=extend_schema(description="Partial video update"),
    destroy=extend_schema(description="Video delete"),
)
@extend_schema(tags=["Video"])
class VideoViewSet(viewsets.ModelViewSet):
    queryset = video_models.Video.objects.all()
    serializer_class = video_serializers.VideoSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        core_permissions.IsObjectOwner,
    ]
