from apps.core.views import ModelViewSet

from . import models, serializers


class CommentViewSet(ModelViewSet):
    queryset = models.Comment.objects.all()
    serializers_class = serializers.CommentCreateSerializer
    actions_serializers_map = {
        "list": serializers.CommentsListSerializer,
    }
