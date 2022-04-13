from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement, UsersFavorite
from advertisements.permissions import IsOwnerOrReadOnly, AddFavoritesOrOwner
from advertisements.serializers import AdvertisementSerializer, UsersFavoriteSerializer


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
        elif self.action == 'add_to_favorites':
            return [IsAuthenticated(), AddFavoritesOrOwner()]
        return [IsOwnerOrReadOnly()]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    @action(detail=True, methods=['POST'])
    def add_to_favorites(self, request, pk):
        user = request.user
        advertisement = Advertisement.objects.filter(pk=pk).first()
        if not advertisement:
            return Response(status=status.HTTP_404_NOT_FOUND)
        in_favorites = UsersFavorite.objects.filter(user=user, advertisement=advertisement)
        if in_favorites:
            return Response('Объявление уже добавлено в избранное')
        else:
            UsersFavorite.objects.create(
                user=user,
                advertisement=advertisement
            )
            return Response('Объявление успешно добавлено в избранное')

    @action(detail=False, methods=['GET'])
    def favorites(self, request):
        user_favorites = UsersFavorite.objects.filter(user=request.user)
        serializer = UsersFavoriteSerializer(user_favorites, many=True)
        return Response(serializer.data)
