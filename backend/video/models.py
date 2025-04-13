from django.db import models

from core import mixins as core_mixins


def video_upload_to(instance, filename):
    return f"USER_{instance.author.id}/VIDEO_{instance.id}/video.{filename.split(".")[-1]}"


def video_preview_upload_to(instance, filename):
    return f"USER_{instance.author.id}/VIDEO_{instance.id}/preview.{filename.split(".")[-1]}"


class Video(core_mixins.CreatedUpdatedMixin):
    video = models.FileField(upload_to=video_upload_to)
    preview = models.ImageField(upload_to=video_preview_upload_to, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    author = models.ForeignKey(
        "core.User", on_delete=models.CASCADE, related_name="uploaded_videos"
    )
    users_watched_video = models.ManyToManyField(
        to="core.User", related_name="watched_videos", through="video.ViewsHistory"
    )
    views_count = models.PositiveIntegerField(default=0)
    users_liked_video = models.ManyToManyField(
        to="core.User", related_name="liked_videos", through="video.LikesHistory"
    )
    likes_count = models.PositiveIntegerField(default=0)
    users_disliked_video = models.ManyToManyField(
        to="core.User", related_name="disliked_videos", through="video.DislikesHistory"
    )
    dislikes_count = models.PositiveIntegerField(default=0)


class AbstractUserVideoModel(models.Model):
    user = models.ForeignKey("core.User", on_delete=models.CASCADE)
    video = models.ForeignKey("video.Video", on_delete=models.CASCADE)
    made_action_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "video")
        abstract = True


class ViewsHistory(AbstractUserVideoModel):
    pass


class LikesHistory(AbstractUserVideoModel):
    pass


class DislikesHistory(AbstractUserVideoModel):
    pass
