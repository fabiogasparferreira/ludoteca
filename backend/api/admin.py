from django.contrib import admin

# Register your models here.
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from backend.api.models import BggGame, Badge, Location

User = get_user_model()

admin.site.register(User, UserAdmin)


@admin.register(BggGame)
class BggGameAdmin(admin.ModelAdmin):
    fields = ('name', 'bggid','badges')
    list_display = ('name', 'bggid', 'rank')
    readonly_fields = ('bggid', 'name',)
    ordering = ('name',)


admin.site.register(Badge)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')
    ordering = ('name', 'type')

