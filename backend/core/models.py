from django.db import models
from django.contrib.auth.models import AbstractUser

from core import mixins as core_mixins


class User(AbstractUser, core_mixins.CreatedUpdatedMixin):
    email = models.EmailField("email", unique=True)
