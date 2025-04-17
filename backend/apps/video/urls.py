from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register("video", views.VideoViewSet)

urlpatterns = router.urls
