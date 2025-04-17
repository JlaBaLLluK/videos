from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser

from . import mixins


def profile_photo_upload_to(instance, filename):
    return f"{instance.id}/logo.{filename.split(".")[-1]}"


class User(AbstractUser, mixins.CreatedUpdatedMixin):
    username_validator = RegexValidator(
        regex=r"^[a-zA-Z][a-zA-Z0-9_]*$",
        message="Имя пользователя может содержать буквы латинского алфавита, цифры и символ нижнего подчеркивания.",
    )
    username = models.CharField(
        unique=True,
        validators=[username_validator],
        max_length=255,
        error_messages={"unique": "Это имя пользователя уже занято."},
    )
    email = models.EmailField(
        unique=True, error_messages={"unique": "Эта почта уже занята."}
    )
    profile_photo = models.ImageField(upload_to=profile_photo_upload_to, blank=True)
    description = models.TextField(blank=True)
    subscriptions = models.ManyToManyField(
        "self", symmetrical=False, related_name="subscribers"
    )

    @property
    def channel_name(self) -> str:
        return (
            f"{self.last_name} {self.first_name}"
            if self.first_name or self.last_name
            else self.username
        )

    @property
    def subscribers_count(self) -> int:
        return self.subscribers.count()

    @property
    def subscriptions_count(self) -> int:
        return self.subscriptions.count()

    @property
    def videos_count(self) -> int:
        return self.uploaded_videos.count()
