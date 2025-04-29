from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from apps.core.views import ModelViewSet
from apps.core import models as core_models
from . import models, serializers


class PlaylistViewSet(ModelViewSet):
    queryset = models.Playlist.objects.all()
    serializer_class = serializers.PlaylistCreateSerializer
    actions_serializers_map = {
        "list": serializers.PlaylistsListSerializer,
        "retrieve": serializers.PlaylistDetailSerializer,
        "partial_update": serializers.PlaylistEditSerializer,
        "playlist_initial": serializers.PlaylistEditSerializer,
    }
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        if self.request.query_params.get("my_playlists"):
            return self.request.user.playlists.order_by("-updated_at")

        if username := self.request.query_params.get("by_username"):
            return get_object_or_404(
                core_models.User, username=username
            ).playlists.order_by("-updated_at")

        return super().get_queryset()

    @action(methods=["GET"], detail=True, url_path="initial")
    def playlist_initial(self, request, *args, **kwargs):
        playlist = self.get_object()
        return Response(self.get_serializer(playlist).data)
