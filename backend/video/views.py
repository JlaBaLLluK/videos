from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response

from core import permissions as core_permissions
from core import mixins as core_mixins
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
class VideoViewSet(
    core_mixins.CreateObjectWithIdInFilePathMixin, viewsets.ModelViewSet
):
    queryset = video_models.Video.objects.all()
    serializer_class = video_serializers.VideoSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        core_permissions.IsObjectOwner,
    ]
    file_fields_and_functions = {
        "video": video_models.video_upload_to,
        "preview": video_models.video_preview_upload_to,
    }
    creator_field = "author"

    def retrieve(self, request, *args, **kwargs):
        video = self.get_object()
        if (
            request.user.is_authenticated
            and request.user not in video.users_watched_video.all()
        ):
            watches_history = video_serializers.WatchesHistorySerializer(
                data={"video": video.id, "user": request.user.id}
            )
            watches_history.is_valid(raise_exception=True)
            watches_history.save()
            video.watches_count += 1
            video.save()

        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        description="Like video by user",
        parameters=[
            OpenApiParameter(
                name="id",
                description="A unique integer value identifying this video.",
                location=OpenApiParameter.PATH,
                required=True,
                type=int,
            )
        ],
    )
    @action(
        methods=["POST"],
        detail=True,
        serializer_class=video_serializers.LikesHistorySerializer,
        permission_classes=[IsAuthenticatedOrReadOnly],
    )
    def like(self, request, pk):
        video = self.get_object()
        serializer = self.get_serializer(data={"video": pk, "user": request.user.id})
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            video.likes_count += 1
            video.users_liked_video.add(request.user)
        except serializers.ValidationError:
            video.likes_count -= 1
            video.users_liked_video.remove(request.user)

        video.save()
        return Response(data=serializer.data)
