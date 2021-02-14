from django.contrib.auth import get_user_model
from django.db.models import Count
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView
from rest_framework import viewsets, permissions, generics
from rest_framework import filters
from django_filters import rest_framework as django_filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt import authentication

from backend.api.filters import LibraryGameFilter
from backend.api.models import LibraryGame, Withdraw, Location, Supplier, BggGame
from backend.api.serializers import LibraryGameSerializer, UserSerializer, PlayerSerializer, WithdrawSerializer, \
    LocationSerializer, SupplierSerializer, BggGameSerializer
from backend.api import utils

User = get_user_model()

# Serve Vue Application
index_view = never_cache(TemplateView.as_view(template_name='index.html'))


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 1000


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.order_by('name')
    serializer_class = SupplierSerializer
    authentication_classes = (authentication.JWTAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    filter_backends = (filters.SearchFilter, django_filters.DjangoFilterBackend)
    search_fields = ['name']


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by('first_name', 'last_name')
    serializer_class = PlayerSerializer
    authentication_classes = (authentication.JWTAuthentication,)
    filter_backends = (filters.SearchFilter, django_filters.DjangoFilterBackend)
    search_fields = ['first_name', 'last_name', 'username', 'email']
    # permission_classes = (permissions.IsAdminUser,)


class LibraryGameViewSet(viewsets.ModelViewSet):
    queryset = LibraryGame.objects.order_by('game__name')
    serializer_class = LibraryGameSerializer
    search_fields = ['game__name', 'game__other_names']
    filter_backends = (filters.SearchFilter, django_filters.DjangoFilterBackend)
    filterset_class = LibraryGameFilter
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    authentication_classes = [authentication.JWTAuthentication]
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        bggid = serializer.initial_data['game_id']
        game = utils.BGGGame.find(bggid)

        if game is None:
            game = utils.BGGGame.create(bggid)

        serializer.is_valid()
        serializer.save(game=game)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = (permissions.IsAdminUser,)

    def get_object(self):
        pk = self.kwargs.get('pk')

        if pk == "current":
            return self.request.user

        return super(UserViewSet, self).get_object()


class WithdrawViewSet(viewsets.ModelViewSet):
    queryset = Withdraw.objects.all()
    serializer_class = WithdrawSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = (permissions.IsAdminUser,)


class StatisticsViewSet(APIView):
    def get(self, request, format=None):
        library_games = {
            "total": LibraryGame.objects.all().count(),
            "being_played": LibraryGame.objects.filter(withdraw__date_returned__isnull=True)
        }

        return Response({"library_games": library_games})


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.order_by('name').all()
    serializer_class = LocationSerializer
