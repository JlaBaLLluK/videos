from rest_framework.routers import SimpleRouter

from core.views import *

router = SimpleRouter()
router.register("users", UserViewSet)

urlpatterns = router.urls
