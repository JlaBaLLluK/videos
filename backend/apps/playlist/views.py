from rest_framework.permissions import IsAuthenticatedOrReadOnly

from apps.core.views import ModelViewSet
from . import models, serializers


class PlaylistViewSet(ModelViewSet):
    queryset = models.Playlist.objects.all()
    serializer_class = serializers.PlaylistCreateSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
