from apps.core.mixins import CreatedUpdatedMixin

from django.db import models


class Comment(CreatedUpdatedMixin):
    author = models.ForeignKey(
        "core.User", on_delete=models.CASCADE, related_name="comments"
    )
    video = models.ForeignKey(
        "video.Video", on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField()
    users_liked_comment = models.ManyToManyField(
        "core.User", related_name="liked_comments"
    )
    likes_count = models.PositiveIntegerField(default=0)
    users_disliked_comment = models.ManyToManyField(
        "core.User", related_name="disliked_comments"
    )
    dislikes_count = models.PositiveIntegerField(default=0)
