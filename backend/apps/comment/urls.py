from rest_framework.routers import DefaultRouter

from apps.comment.views import CommentViewSet

router = DefaultRouter("comments/", CommentViewSet)

urlpatterns = router.urls
