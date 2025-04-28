from django.db import models

from apps.core import mixins as core_mixins


class Playlist(core_mixins.CreatedUpdatedMixin):
    name = models.CharField(max_length=255)
    videos = models.ManyToManyField(to="video.Video", related_name="playlists")
