from django.db import models
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from rest_framework import serializers


class ActionsSerializersMapMixin:
    actions_serializers_map: dict

    def get_serializer_class(self):
        return (
            self.actions_serializers_map[self.action]
            if self.action in self.actions_serializers_map
            else super().get_serializer_class()
        )


class ActionsPermissionsMapMixin:
    actions_permissions_map: dict

    def get_permissions(self):
        if self.action in self.actions_permissions_map:
            self.permission_classes = self.actions_permissions_map[self.action]

        return super().get_permissions()


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
            if not serializer.validated_data.get(file_field_name):
                continue

            file_field = serializer.validated_data[file_field_name]
            file_content = ContentFile(file_field.read())
            file_path = filename_function(instance, file_field.name)
            setattr(instance, file_field_name, file_path)
            instance.save()
            default_storage.save(file_path, file_content)


class UserSerializerMixin(metaclass=serializers.SerializerMetaclass):
    description_preview = serializers.SerializerMethodField()
    is_request_user_subscribed = serializers.SerializerMethodField()

    @staticmethod
    def get_description_preview(instance):
        description_parts = instance.description.split()
        description_preview_parts = description_parts[:40]
        if len(description_preview_parts) < len(description_parts):
            description_preview_parts[-1] += "..."

        return " ".join(description_preview_parts)

    def get_is_request_user_subscribed(self, instance):
        user = self.context["request"].user
        return user.is_authenticated and user in instance.subscribers.all()
