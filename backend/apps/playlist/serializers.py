from rest_framework import serializers

from . import models
from apps.video import serializers as video_serializers


class PlaylistCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Playlist
        fields = ("name",)

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class PlaylistsListSerializer(serializers.ModelSerializer):
    playlist_preview = serializers.SerializerMethodField()
    videos_count = serializers.SerializerMethodField()

    class Meta:
        model = models.Playlist
        fields = ("name", "playlist_preview", "videos_count", "id")

    @staticmethod
    def get_playlist_preview(obj):
        first_video = obj.videos.through.objects.order_by("-add_date").first()
        return first_video.preview if first_video else None

    @staticmethod
    def get_videos_count(obj):
        return obj.videos.count()


class PlaylistEditSerializer(serializers.ModelSerializer):
    videos = serializers.SerializerMethodField()
    videos_outside_playlist = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Playlist
        fields = ("name", "videos", "videos_outside_playlist")

    def get_videos(self, obj):
        return video_serializers.VideosListSerializer(
            obj.videos, many=True, context=self.context
        ).data

    def get_videos_outside_playlist(self, obj):
        queryset = self.context["request"].user.uploaded_videos.exclude(
            id__in=obj.videos.values_list("id", flat=True)
        )
        return video_serializers.VideosListSerializer(
            queryset, many=True, context=self.context
        ).data
