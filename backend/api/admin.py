from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from backend.api.models import BggGame, Badge, Location, User

admin.site.register(User, UserAdmin)


@admin.register(BggGame)
class BggGameAdmin(admin.ModelAdmin):
    fields = ('name', 'bggid', 'badges',)
    readonly_fields = ('bggid', 'name',)
    ordering = ('name',)


admin.site.register(Badge)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    ordering = ('name',)

