from rest_framework import serializers

from . import models
from apps.core import serializers_fields


class VideoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Video
        fields = ("title", "description", "preview", "video")
        extra_kwargs = {
            "video": {
                "error_messages": {
                    "required": "Видео не выбрано.",
                }
            }
        }


class VideosListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Video
        fields = ("id", "title", "preview", "views_count")


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
