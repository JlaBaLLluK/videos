from rest_framework import serializers

from . import models


class PlaylistCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Playlist
        fields = ("name",)
