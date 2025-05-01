from rest_framework import serializers


from . import models, mixins
from apps.core import serializers as core_serializers
from apps.core import mixins as core_mixins
from apps.core import utils as core_utils
from apps.comment import serializers as comment_serializers


class VideoEditSerializer(
    core_mixins.SetEmptyFileSerializerMixin, serializers.ModelSerializer
):
    file_fields = ["preview"]

    class Meta:
        model = models.Video
        fields = ("title", "description", "preview")

    def get_fields(self):
        fields = super().get_fields()
        fields["preview"].required = False
        return fields


class VideoCreateSerializer(VideoEditSerializer):
    class Meta(VideoEditSerializer.Meta):
        model = models.Video
        fields = VideoEditSerializer.Meta.fields + ("video",)
        extra_kwargs = {
            "video": {
                "error_messages": {
                    "required": "Видео не выбрано.",
                }
            }
        }


class VideosListSerializer(mixins.VideoSerializerMixin, serializers.ModelSerializer):
    author_channel_name = serializers.CharField(source="author.channel_name")
    author_profile_photo = serializers.ImageField(source="author.profile_photo")
    author_username = serializers.CharField(source="author.username")

    class Meta:
        model = models.Video
        fields = (
            "id",
            "title",
            "preview",
            "views_count",
            "published_ago",
            "author_channel_name",
            "author_profile_photo",
            "author_username",
        )


class VideoDetailSerializer(mixins.VideoSerializerMixin, serializers.ModelSerializer):
    description_preview = serializers.SerializerMethodField()
    author = core_serializers.UserDetailSerializer()
    is_request_user_liked = serializers.SerializerMethodField()
    is_request_user_disliked = serializers.SerializerMethodField()
    comments = comment_serializers.CommentsListSerializer(many=True)

    class Meta:
        model = models.Video
        fields = "__all__"

    @staticmethod
    def get_description_preview(obj):
        return core_utils.get_text_preview(obj.description, words_count=35)

    def get_is_request_user_liked(self, obj):
        return (
            self.context["request"].user.is_authenticated
            and self.context["request"].user in obj.users_liked_video.all()
        )

    def get_is_request_user_disliked(self, obj):
        return (
            self.context["request"].user.is_authenticated
            and self.context["request"].user in obj.users_disliked_video.all()
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["likes_count"] = core_utils.get_number_representation(instance.likes_count)
        data["dislikes_count"] = core_utils.get_number_representation(
            instance.dislikes_count
        )
        return data
