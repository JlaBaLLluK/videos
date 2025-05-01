from rest_framework import serializers

from . import models

from apps.core import utils as core_utils
from apps.core import serializers as core_serializers


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ("text", "video")

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)


class CommentsListSerializer(serializers.ModelSerializer):
    author = core_serializers.UserListSerializer()
    text_preview = serializers.SerializerMethodField()
    published_ago = serializers.SerializerMethodField()

    class Meta:
        model = models.Comment
        fields = "__all__"

    @staticmethod
    def get_text_preview(obj):
        return core_utils.get_text_preview(obj.text, words_count=25)

    @staticmethod
    def get_published_ago(obj):
        return core_utils.get_creation_date_representation(obj.created_at)

    def to_representation(self, obj):
        data = super().to_representation(obj)
        data["likes_count"] = core_utils.get_number_representation(obj.likes_count)
        data["dislikes_count"] = core_utils.get_number_representation(
            obj.dislikes_count
        )
        return data
