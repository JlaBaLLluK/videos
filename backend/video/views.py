from django.db import IntegrityError
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from rest_framework import viewsets
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
            video.users_watched_video.add(request.user)
            video.watches_count += 1
            video.save()

        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        description="Like video by user",
    )
    @action(
        methods=["POST"],
        detail=True,
        permission_classes=[IsAuthenticatedOrReadOnly],
    )
    def like(self, request, pk):
        video = self.get_object()
        try:
            video_models.LikesHistory.objects.create(
                video=video, user=request.user
            )  # add doesn't throw an exception
            response_message = "Set like"
            video.likes_count += 1
            if request.user in video.users_disliked_video.all():
                video.dislikes_count -= 1
                video.users_disliked_video.remove(request.user)

        except IntegrityError:
            video.users_liked_video.remove(request.user)
            response_message = "Removed like"
            video.likes_count -= 1

        video.save()
        return Response({"success": response_message})

    @extend_schema(
        description="Dislike video by user",
    )
    @action(
        methods=["POST"],
        detail=True,
        permission_classes=[IsAuthenticatedOrReadOnly],
    )
    def dislike(self, request, pk):
        video = self.get_object()
        try:
            video_models.DislikesHistory.objects.create(
                video=video, user=request.user
            )  # add doesn't throw an exception
            response_message = "Set dislike"
            video.dislikes_count += 1
            if request.user in video.users_liked_video.all():
                video.likes_count -= 1
                video.users_liked_video.remove(request.user)

        except IntegrityError:
            video.users_disliked_video.remove(request.user)
            response_message = "Removed dislike"
            video.dislikes_count -= 1

        video.save()
        return Response({"success": response_message})
