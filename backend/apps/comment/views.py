from apps.core.views import ModelViewSet

from . import models, serializers


class CommentViewSet(ModelViewSet):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentCreateSerializer
    actions_serializers_map = {
        "list": serializers.CommentsListSerializer,
    }
    sort_orders = {"0": "", "1": "-"}

    def get_queryset(self):
        if video_id := self.request.query_params.get("by_video"):
            queryset = super().get_queryset().filter(video_id=video_id)
            sort_by = self.request.query_params.get("sort_by", "")
            sort_order = self.sort_orders.get(
                self.request.query_params.get("is_descending_order"), ""
            )
            if sort_by and sort_order:
                return queryset.order_by(f"{sort_order}{sort_by}")

            return queryset

        return super().get_queryset()
