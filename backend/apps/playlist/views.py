from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from apps.core.views import ModelViewSet
from . import models, serializers


class PlaylistViewSet(ModelViewSet):
    queryset = models.Playlist.objects.all()
    serializer_class = serializers.PlaylistCreateSerializer
    actions_serializers_map = {
        "list": serializers.PlaylistsListSerializer,
        "partial_update": serializers.PlaylistEditSerializer,
        "playlist_initial": serializers.PlaylistEditSerializer,
    }
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(user=self.request.user)
            .order_by("-updated_at")
        )

    @action(methods=["GET"], detail=True, url_path="initial")
    def playlist_initial(self, request, *args, **kwargs):
        playlist = self.get_object()
        return Response(self.get_serializer(playlist).data)
