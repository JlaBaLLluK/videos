from django.db import models

from apps.core import mixins as core_mixins


class Playlist(core_mixins.CreatedUpdatedMixin):
    name = models.CharField(max_length=255)
    videos = models.ManyToManyField(
        to="video.Video", related_name="playlists", through="PlaylistVideo"
    )
    user = models.ForeignKey(
        to="core.User", related_name="playlists", on_delete=models.CASCADE
    )


class PlaylistVideo(models.Model):
    add_date = models.DateTimeField(auto_now_add=True)
    video = models.ForeignKey(
        to="video.Video", on_delete=models.CASCADE, related_name="playlist_video"
    )
    playlist = models.ForeignKey(
        to=Playlist, on_delete=models.CASCADE, related_name="playlist_video"
    )
