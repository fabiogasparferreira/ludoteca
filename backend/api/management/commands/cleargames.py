from django.core.management.base import BaseCommand

from backend.api.models import LibraryGame, Withdraw, Location, User


class Command(BaseCommand):

    def handle(self, *args, **options):
        for w in Withdraw.objects.all():
            w.delete()

        for g in LibraryGame.objects.all():
            g.delete()

        for p in User.objects.filter(is_superuser=False):
            p.delete()

        for l in Location.objects.all():
            l.delete()
