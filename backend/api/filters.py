from django.db.models import Count, Q
from django_filters import rest_framework as filters

from backend.api.models import LibraryGame


class LibraryGameFilter(filters.FilterSet):
    LIBRARY_GAMES_STATUS_CHOICES = (
        ('available', 'available'),
        ('not-checked-in', 'not-checked-in'),
        ('not-available', 'not-available')
    )

    min_players = filters.NumberFilter(field_name='game__min_players', lookup_expr='gte')
    max_players = filters.NumberFilter(field_name='game__max_players', lookup_expr='lte')
    min_playtime = filters.NumberFilter(field_name='game__min_playtime', lookup_expr='gte')
    max_playtime = filters.NumberFilter(field_name='game__max_playtime', lookup_expr='lte')
    status = filters.ChoiceFilter(method='filter_status', choices=LIBRARY_GAMES_STATUS_CHOICES)

    class Meta:
        model = LibraryGame
        fields = ['owner', 'location']

    def filter_status(self, queryset, name, value):
        if value == 'not-checked-in':
            queryset = queryset.filter(date_checkin__isnull=True)
        elif value == 'available':
            queryset = queryset.filter(date_checkin__isnull=False).annotate(
                open_withdraws=Count('withdraw', filter=Q(withdraw__date_returned__isnull=True))).filter(
                open_withdraws__exact=0)
        elif value == 'not-available':
            queryset = queryset.filter(date_checkin__isnull=False).annotate(
                open_withdraws=Count('withdraw', filter=Q(withdraw__date_returned__isnull=True))).filter(
                open_withdraws__gt=0)
        print(str(list(queryset.all())))
        return queryset
