from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register("videos", views.VideoViewSet)

urlpatterns = [
    path("play-video/<int:pk>/", views.stream_video_view, name="play_video")
] + router.urls
