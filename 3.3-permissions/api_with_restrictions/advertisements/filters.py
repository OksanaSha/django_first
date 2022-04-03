from django_filters import rest_framework as filters

from advertisements.models import Advertisement


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""

    creator = filters.NumberFilter()
    created_at = filters.DateFromToRangeFilter()

    class Meta:
        model = Advertisement
        fields = ['creator', 'created_at']

