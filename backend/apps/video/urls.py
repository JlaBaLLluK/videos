from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register("videos", views.VideoViewSet)

urlpatterns = router.urls
