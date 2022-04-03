from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement
from advertisements.permissions import IsOwnerOrReadOnly
from advertisements.serializers import AdvertisementSerializer

class CreatorFilter(DjangoFilterBackend):
    pass

class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    def get_queryset(self):
        queryset = Advertisement.objects.filter(status='OPEN')
        creator = self.request.query_params.get('creator', None)
        if creator:
            queryset_closed = Advertisement.objects.filter(status='CLOSED')
            queryset |= queryset_closed
        if self.request.user.is_authenticated:
            queryset_draft = Advertisement.objects.filter(creator=self.request.user, status='DRAFT')
            queryset |= queryset_draft
        return queryset

    # queryset = Advertisement.objects.exclude(status='DRAFT')
    serializer_class = AdvertisementSerializer
    filterset_class = AdvertisementFilter
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsOwnerOrReadOnly]

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        return [IsOwnerOrReadOnly()]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)