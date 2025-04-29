from rest_framework import serializers

from . import models
from apps.video import serializers as video_serializers
from apps.video import models as video_models


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
        fields = ("name", "videos_count", "id", "playlist_preview")

    def get_playlist_preview(self, obj):
        video_playlist = (
            obj.videos.through.objects.filter(playlist=obj).order_by("add_date").first()
        )
        if not video_playlist:
            return None

        video = video_playlist.video
        return self.context["request"].build_absolute_uri(video.preview.url)

    @staticmethod
    def get_videos_count(obj):
        return obj.videos.count()


class PlaylistDetailSerializer(serializers.ModelSerializer):
    videos = video_serializers.VideosListSerializer(many=True, read_only=True)

    class Meta:
        model = models.Playlist
        fields = ("name", "videos")


class PlaylistEditSerializer(serializers.ModelSerializer):
    videos = serializers.PrimaryKeyRelatedField(
        queryset=video_models.Video.objects.all(), many=True
    )
    videos_in_playlist = video_serializers.VideosListSerializer(
        many=True, source="videos", read_only=True
    )
    videos_outside_playlist = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Playlist
        fields = ("name", "videos", "videos_outside_playlist", "videos_in_playlist")

    def get_videos_outside_playlist(self, obj):
        queryset = self.context["request"].user.uploaded_videos.exclude(
            id__in=obj.videos.values_list("id", flat=True)
        )
        return video_serializers.VideosListSerializer(
            queryset, many=True, context=self.context
        ).data
