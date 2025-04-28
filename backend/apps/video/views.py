from django.db import IntegrityError
from django.db.models import F
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core import permissions as core_permissions
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
    }
    authentication_classes = [authentication.JwtAuthenticationNoException]
    file_fields_and_functions = {
        "video": models.video_upload_to,
        "preview": models.video_preview_upload_to,
    }
    creator_field = "author"

    def perform_create(self, serializer):
        super().perform_create(serializer)
        if not serializer.instance.preview:
            utils.generate_preview(serializer.instance)

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
            utils.generate_preview(instance)

    @extend_schema(description="Like video by user")
    @action(methods=["POST"], detail=True)
    def like(self, request, *args, **kwargs):
        video = self.get_object()
        try:
            models.LikesHistory.objects.create(
                video=video, user=request.user
            )  # 'add' method doesn't throw an exception
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
        return Response({"message": response_message})

    @extend_schema(description="Dislike video by user")
    @action(methods=["POST"], detail=True)
    def dislike(self, request, *args, **kwargs):
        video = self.get_object()
        try:
            models.DislikesHistory.objects.create(
                video=video, user=request.user
            )  # 'add' method doesn't throw an exception
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
        return Response({"message": response_message})

    @extend_schema(description="List of disliked by user videos")
    @action(methods=["GET"], detail=False, url_path="my-watched")
    def watched_by_user(self, request):
        serializer = self.get_serializer(
            instance=request.user.watched_videos.order_by("-made_action_at"), many=True
        )
        return Response(serializer.data)

    @extend_schema(description="List of liked by user videos")
    @action(methods=["GET"], detail=False, url_path="my-liked")
    def liked_by_user(self, request):
        serializer = self.get_serializer(
            instance=request.user.liked_videos.order_by("-made_action_at"), many=True
        )
        return Response(serializer.data)

    @extend_schema(description="List of uploaded by user videos")
    @action(methods=["GET"], detail=False, url_path="my-published")
    def user_videos(self, request):
        serializer = self.get_serializer(
            instance=request.user.uploaded_videos.order_by("-created_at"), many=True
        )
        return Response(serializer.data)

    @action(methods=["GET", "POST"], detail=False, url_path="watch-later")
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
