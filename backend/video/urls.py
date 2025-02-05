from rest_framework.routers import SimpleRouter

from video.views import *

router = SimpleRouter()
router.register("video", VideoViewSet)

urlpatterns = router.urls
