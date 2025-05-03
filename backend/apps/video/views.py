from django.db import IntegrityError
from django.db.models import F
from django.http import FileResponse, StreamingHttpResponse
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.settings import api_settings

from apps.core import permissions as core_permissions, models as core_models
from apps.core import authentication
from apps.core import mixins as core_mixins
from apps.core.views import ModelViewSet
from . import serializers, models, utils


@extend_schema_view(
    list=extend_schema(description="List or videos"),
    create=extend_schema(description="Upload new video"),
    retrieve=extend_schema(description="Get single video by id"),
    update=extend_schema(description="Video update"),
    partial_update=extend_schema(description="Partial video update"),
    destroy=extend_schema(description="Video delete"),
)
@extend_schema(tags=["Video"])
class VideoViewSet(core_mixins.CreateObjectWithIdInFilePathMixin, ModelViewSet):
    queryset = models.Video.objects.all()
    serializer_class = serializers.VideoCreateSerializer
    actions_serializers_map = {
        "list": serializers.VideosListSerializer,
        "retrieve": serializers.VideoDetailSerializer,
        "partial_update": serializers.VideoEditSerializer,
        "watched_by_user": serializers.VideosListSerializer,
        "liked_by_user": serializers.VideosListSerializer,
        "user_videos": serializers.VideosListSerializer,
        "watch_later": serializers.VideosListSerializer,
    }
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        core_permissions.IsObjectOwnerOrReadonly,
    ]
    actions_permissions_map = {
        "like": [IsAuthenticated],
        "dislike": [IsAuthenticated],
        "watched_by_user": [IsAuthenticated],
        "liked_by_user": [IsAuthenticated],
        "user_videos": [IsAuthenticated],
        "watch_later": [IsAuthenticated],
        "remove_from_history": [IsAuthenticated],
    }
    authentication_classes = [authentication.JwtAuthenticationNoException]
    file_fields_and_functions = {
        "video": models.video_upload_to,
        "preview": models.video_preview_upload_to,
    }
    creator_field = "author"

    def get_authenticators(self):
        if (
            self.request.GET.get("my-published")
            or self.request.GET.get("views_history")
            or self.request.GET.get("likes_history")
        ):
            self.authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES

        return super().get_authenticators()

    def get_queryset(self):
        if self.request.query_params.get("my-published"):
            return self.request.user.uploaded_videos.order_by("-created_at")

        if username := self.request.query_params.get("by_username"):
            return get_object_or_404(
                core_models.User, username=username
            ).uploaded_videos.order_by("-created_at")

        if self.request.query_params.get("likes_history"):
            return self.request.user.liked_videos.all()

        if self.request.query_params.get("views_history"):
            return self.request.user.watched_videos.all()

        return super().get_queryset()

    def perform_create(self, serializer):
        super().perform_create(serializer)
        if not serializer.instance.preview:
            utils.generate_preview(serializer.instance)

        utils.prepare_file(serializer.instance)

    def retrieve(self, request, *args, **kwargs):
        video = self.get_object()
        if request.query_params.get("isInitialReceive"):
            serializer = self.actions_serializers_map["partial_update"](instance=video)
            return Response(serializer.data)

        if (
            request.user.is_authenticated
            and request.user not in video.users_watched_video.all()
        ):
            video.users_watched_video.add(request.user)
            video.views_count += 1
            video.save()

        return super().retrieve(request, *args, **kwargs)

    def perform_update(self, serializer):
        instance = self.get_object()
        instance.preview.delete(save=False)
        super().perform_update(serializer)
        if not serializer.instance.preview:
            utils.generate_preview(serializer.instance)

    @extend_schema(description="Like video by user")
    @action(
        methods=["POST"],
        detail=True,
        authentication_classes=api_settings.DEFAULT_AUTHENTICATION_CLASSES,
    )
    def like(self, request, *args, **kwargs):
        video = self.get_object()
        try:
            models.LikesHistory.objects.create(
                video=video, user=request.user
            )  # 'add' method doesn't throw an exception
            is_set = True
            video.likes_count += 1
            if request.user in video.users_disliked_video.all():
                video.dislikes_count -= 1
                video.users_disliked_video.remove(request.user)

        except IntegrityError:
            video.users_liked_video.remove(request.user)
            is_set = False
            video.likes_count -= 1

        video.save()
        return Response(
            {
                "is_set": is_set,
                "new_likes_count": video.likes_count,
                "new_dislikes_count": video.dislikes_count,
            }
        )

    @extend_schema(description="Dislike video by user")
    @action(
        methods=["POST"],
        detail=True,
        authentication_classes=api_settings.DEFAULT_AUTHENTICATION_CLASSES,
    )
    def dislike(self, request, *args, **kwargs):
        video = self.get_object()
        try:
            models.DislikesHistory.objects.create(
                video=video, user=request.user
            )  # 'add' method doesn't throw an exception
            is_set = True
            video.dislikes_count += 1
            if request.user in video.users_liked_video.all():
                video.likes_count -= 1
                video.users_liked_video.remove(request.user)

        except IntegrityError:
            video.users_disliked_video.remove(request.user)
            is_set = False
            video.dislikes_count -= 1

        video.save()
        return Response(
            {
                "is_set": is_set,
                "new_dislikes_count": video.dislikes_count,
                "new_likes_count": video.likes_count,
            }
        )

    @action(
        methods=["GET", "POST"],
        detail=False,
        url_path="watch-later",
        authentication_classes=api_settings.DEFAULT_AUTHENTICATION_CLASSES,
    )
    def watch_later(self, request):
        if request.method == "GET":
            watch_later_videos_with_action_date = (
                request.user.videos_to_watch_later.annotate(
                    made_action_at=F("watchlater__made_action_at")
                ).order_by("-made_action_at")
            )
            serializer = self.get_serializer(
                instance=watch_later_videos_with_action_date, many=True
            )
            return Response(serializer.data)

        video_id = request.data["video_id"]
        video = models.Video.objects.get(pk=video_id)
        if request.user not in video.watch_later_users.all():
            video.watch_later_users.add(request.user, through_defaults={})
            message = 'Видео добавлено в плейлист "Смотреть позже"'
        else:
            video.watch_later_users.remove(request.user)
            message = 'Видео убрано из плейлиста "Смотреть позже"'

        return Response({"message": message})

    @action(
        methods=["PUT"],
        detail=True,
        authentication_classes=api_settings.DEFAULT_AUTHENTICATION_CLASSES,
        url_path="remove-from-history",
    )
    def remove_from_history(self, request, *args, **kwargs):
        video = self.get_object()
        video.users_watched_video.remove(request.user)
        return Response()


def stream_video_view(request, pk):
    video = get_object_or_404(models.Video, pk=pk)
    file_path = video.video.path
    file_size = video.video.size
    range_header = request.headers.get("Range")
    if not range_header:
        return FileResponse(open(file_path, "rb"), content_type="video/mp4")

    start_bytes, end_bytes = range_header.replace("bytes=", "").split("-")
    start = int(start_bytes) if start_bytes else 0
    end = int(end_bytes) if end_bytes else min(start + 1024 * 1024, file_size - 1)
    range_length = end - start + 1

    # оптимизация: не за раз прочитать сколько запросили, а за несколько (меньший объем занимается результатом read)
    # def file_part_generator(path, offset, length, chunk_size=8192):
    #     with open(path, "rb") as f:
    #         f.seek(offset)
    #         remaining = length
    #         while remaining > 0:
    #             chunk = f.read(min(chunk_size, remaining))
    #             if not chunk:
    #                 break
    #             yield chunk
    #             remaining -= len(chunk)

    response = StreamingHttpResponse(
        file_part_generator(file_path, start, range_length),
        status=206,
        content_type="video/mp4",
    )
    response["Content-Range"] = f"bytes {start}-{end}/{file_size}"
    response["Content-Length"] = str(range_length)
    response["Accept-Ranges"] = "bytes"
    response["Content-Disposition"] = 'inline; filename="video.mp4"'
    return response


def file_part_generator(path, start_offset, read_size):
    with open(path, "rb") as f:
        f.seek(start_offset)
        file_part = f.read(read_size)
        yield file_part
