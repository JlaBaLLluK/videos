from rest_framework import serializers
from django.utils import timezone

from . import models
from apps.core import serializers_fields
from apps.core import mixins as core_mixins


class VideoEditSerializer(
    core_mixins.SetEmptyFileSerializerMixin, serializers.ModelSerializer
):
    file_fields = ["preview"]

    class Meta:
        model = models.Video
        fields = ("title", "description", "preview")

    def get_fields(self):
        fields = super().get_fields()
        fields["preview"].required = False
        return fields


class VideoCreateSerializer(VideoEditSerializer):
    class Meta(VideoEditSerializer.Meta):
        model = models.Video
        fields = VideoEditSerializer.Meta.fields + ("video",)
        extra_kwargs = {
            "video": {
                "error_messages": {
                    "required": "Видео не выбрано.",
                }
            }
        }


class VideosListSerializer(serializers.ModelSerializer):
    published_ago = serializers.SerializerMethodField()
    author_channel_name = serializers.CharField(source="author.channel_name")
    author_profile_photo = serializers.ImageField(source="author.profile_photo")
    author_username = serializers.CharField(source="author.username")

    class Meta:
        model = models.Video
        fields = (
            "id",
            "title",
            "preview",
            "views_count",
            "published_ago",
            "author_channel_name",
            "author_profile_photo",
            "author_username",
        )

    @staticmethod
    def get_published_ago(obj):
        time_passed = timezone.now() - obj.created_at
        days = time_passed.days
        seconds = time_passed.seconds
        if days >= 365:
            return f"{days // 365} г. назад"

        if days >= 30:
            return f"{days // 30} мес. назад"

        if days >= 1:
            return f"{days} д. назад"

        if seconds >= 3600:
            return f"{seconds // 3600} ч. назад"

        return f"{seconds // 60} мин. назад"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        views_placeholder = ""
        if data["views_count"] >= 1_000_000:
            views_placeholder = "млн."
            data["views_count"] //= 1_000_000
        elif data["views_count"] >= 1_000:
            views_placeholder = "тыс."
            data["views_count"] //= 1_000

        data["views_count"] = f'{data["views_count"]} {views_placeholder}'
        return data


class VideoDetailSerializer(serializers.ModelSerializer):
    author = serializers_fields.UserReadOnlyField()

    class Meta:
        model = models.Video
        fields = "__all__"

    def get_fields(self):
        fields = super().get_fields()
        fields["views_count"].read_only = True
        fields["likes_count"].read_only = True
        fields["dislikes_count"].read_only = True
        return fields


class WatchesHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ViewsHistory
        fields = ("user", "video")


class LikesHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LikesHistory
        fields = ("user", "video")
