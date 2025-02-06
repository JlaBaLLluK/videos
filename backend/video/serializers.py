from rest_framework import serializers

from video import models as video_models
from core import serializers_fields


class VideoSerializer(serializers.ModelSerializer):
    author = serializers_fields.UserReadOnlyField()

    class Meta:
        model = video_models.Video
        fields = "__all__"

    def get_fields(self):
        fields = super().get_fields()
        fields["watches_count"].read_only = True
        fields["likes_count"].read_only = True
        fields["dislikes_count"].read_only = True
        return fields


class WatchesHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = video_models.WatchesHistory
        fields = "__all__"


class LikesHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = video_models.LikesHistory
        fields = "__all__"
