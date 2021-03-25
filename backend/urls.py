"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from .api.views import index_view
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from django.http import FileResponse
from backend.api import views

router = routers.DefaultRouter()
router.register(r'library/games', views.LibraryGameViewSet)
router.register(r'library/withdraw', views.WithdrawViewSet)
router.register(r'library/locations', views.LocationViewSet)
router.register(r'store/suppliers', views.SupplierViewSet)
router.register(r'store/games', views.StoreGameViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'players', views.PlayerViewSet)
router.register(r'configurations', views.ConfigurationViewSet)

urlpatterns = [
    path('', index_view, name='index'),

    path('auth/', include('rest_framework.urls')),

    # http://localhost:8000/api/admin/
    path('admin/', admin.site.urls),

    # http://localhost:8000/api/<router-viewsets>
    path('api/', include(router.urls)),

    # Authentication endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

    path('<path:path>', index_view),
]


def index_view(request, path):
    return FileResponse(open('/public/index.html', 'rb'))
