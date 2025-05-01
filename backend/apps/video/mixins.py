from rest_framework import serializers

from apps.core import utils as core_utils


class VideoSerializerMixin(metaclass=serializers.SerializerMetaclass):
    published_ago = serializers.SerializerMethodField()

    @staticmethod
    def get_published_ago(obj):
        return core_utils.get_creation_date_representation(obj.created_at)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["views_count"] = core_utils.get_number_representation(data["views_count"])
        return data
