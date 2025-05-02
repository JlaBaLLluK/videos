from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.settings import api_settings

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

    @action(
        methods=["POST"],
        detail=True,
        authentication_classes=api_settings.DEFAULT_AUTHENTICATION_CLASSES,
    )
    def like(self, request, *args, **kwargs):
        comment = self.get_object()
        if request.user in comment.users_liked_comment.all():
            comment.likes_count -= 1
            is_set = False
            comment.users_liked_comment.remove(request.user)
        else:
            is_set = True
            comment.users_liked_comment.add(request.user)
            comment.likes_count += 1
            if request.user in comment.users_disliked_comment.all():
                comment.users_disliked_comment.remove(request.user)
                comment.dislikes_count -= 1

        comment.save()
        return Response(
            {
                "is_set": is_set,
                "new_likes_count": comment.likes_count,
                "new_dislikes_count": comment.dislikes_count,
            }
        )

    @action(
        methods=["POST"],
        detail=True,
        authentication_classes=api_settings.DEFAULT_AUTHENTICATION_CLASSES,
    )
    def dislike(self, request, *args, **kwargs):
        comment = self.get_object()
        if request.user in comment.users_disliked_comment.all():
            comment.dislikes_count -= 1
            is_set = False
            comment.users_disliked_comment.remove(request.user)
        else:
            is_set = True
            comment.users_disliked_comment.add(request.user)
            comment.dislikes_count += 1
            if request.user in comment.users_liked_comment.all():
                comment.users_liked_comment.remove(request.user)
                comment.likes_count -= 1

        comment.save()
        return Response(
            {
                "is_set": is_set,
                "new_likes_count": comment.likes_count,
                "new_dislikes_count": comment.dislikes_count,
            }
        )
