from rest_framework import serializers
from video import models as video_models


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = video_models.Video
        fields = "__all__"


class WatchesHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = video_models.WatchesHistory
        fields = "__all__"


class LikesHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = video_models.LikesHistory
        fields = "__all__"
