from rest_framework import serializers

from apps.video import models as video_models
from apps.core import serializers_fields


class VideoSerializer(serializers.ModelSerializer):
    author = serializers_fields.UserReadOnlyField()

    class Meta:
        model = video_models.Video
        fields = "__all__"
        extra_kwargs = {
            "video": {
                "error_messages": {
                    "required": "Видео не выбрано",
                }
            }
        }

    def get_fields(self):
        fields = super().get_fields()
        fields["views_count"].read_only = True
        fields["likes_count"].read_only = True
        fields["dislikes_count"].read_only = True
        return fields


class WatchesHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = video_models.ViewsHistory
        fields = ("user", "video")


class LikesHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = video_models.LikesHistory
        fields = ("user", "video")
