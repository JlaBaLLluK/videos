from django.db import models
from django.contrib.auth.models import AbstractUser

from core import mixins as core_mixins


def profile_photo_upload_to(instance, filename):
    return f"{instance.id}/logo.{filename.split(".")[-1]}"


class User(AbstractUser, core_mixins.CreatedUpdatedMixin):
    email = models.EmailField(unique=True)
    profile_photo = models.ImageField(upload_to=profile_photo_upload_to, blank=True)

    @property
    def channel_name(self):
        return f"{self.last_name} {self.first_name}" if self.first_name or self.last_name else self.username
