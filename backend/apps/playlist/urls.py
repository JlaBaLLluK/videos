from rest_framework.routers import DefaultRouter

from apps.playlist.views import PlaylistViewSet

router = DefaultRouter()
router.register("playlists", PlaylistViewSet, basename="playlist")

urlpatterns = router.urls
