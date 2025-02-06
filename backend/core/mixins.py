from django.db import models
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


class CreatedUpdatedMixin(models.Model):
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата редактирования", auto_now=True)

    class Meta:
        abstract = True


class CreateObjectWithIdInFilePathMixin:
    file_fields_and_functions = {}
    creator_field = ""

    def perform_create(self, serializer):
        """
        Create object. If there is no file, we save with no additional actions
        Otherwise need to generate ID to use it in file path.
        """
        author = (
            {self.creator_field: serializer.context["request"].user}
            if self.creator_field
            else {}
        )
        empty_file_names = {
            file_field: "" for file_field in self.file_fields_and_functions
        }
        instance = serializer.save(**empty_file_names, **author)
        for (
            file_field_name,
            filename_function,
        ) in self.file_fields_and_functions.items():
            if not serializer.validated_data[file_field_name]:
                continue

            file_field = serializer.validated_data[file_field_name]
            file_content = ContentFile(file_field.read())
            file_path = filename_function(instance, file_field.name)
            setattr(instance, file_field_name, file_path)
            instance.save()
            default_storage.save(file_path, file_content)
