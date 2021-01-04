from django_filters import rest_framework as filters

from backend.api.models import LibraryGame


class LibraryGameFilter(filters.FilterSet):
    status = filters.CharFilter(field_name='status')

    class Meta:
        model = LibraryGame
        fields = ['owner', 'location']
