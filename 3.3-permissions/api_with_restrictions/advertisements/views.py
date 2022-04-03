from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement
from advertisements.permissions import IsOwnerOrReadOnly
from advertisements.serializers import AdvertisementSerializer

class CreatorFilter(DjangoFilterBackend):
    pass

class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    def get_queryset(self):
        creator = self.request.query_params.get('creator', None)
        if creator:
            queryset = Advertisement.objects.all()
        else:
            queryset = Advertisement.objects.filter(status='OPEN')
        return queryset

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filterset_class = AdvertisementFilter
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsOwnerOrReadOnly]


    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)