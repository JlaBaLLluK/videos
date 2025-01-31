from django.db import models


class CreatedUpdatedMixin(models.Model):
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата редактирования", auto_now=True)

    class Meta:
        abstract = True
