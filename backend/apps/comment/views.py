from apps.core.views import ModelViewSet

from . import models, serializers


class CommentViewSet(ModelViewSet):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentCreateSerializer
    actions_serializers_map = {
        "list": serializers.CommentsListSerializer,
    }

    def get_queryset(self):
        if video_id := self.request.query_params.get("by_video"):
            return super().get_queryset().filter(video_id=video_id)

        return super().get_queryset()
