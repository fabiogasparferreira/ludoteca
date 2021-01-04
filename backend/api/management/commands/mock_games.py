
import random


from boardgamegeek import BGGClient
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from backend.api.models import LibraryGame, Withdraw, Location

User = get_user_model()

bgg = BGGClient()


class Command(BaseCommand):

    def handle(self, *args, **options):
        shelves = Location.objects.all()

        statuses = ['not-checkedin', 'available', 'not-available', 'checkedout']

        for game in LibraryGame.objects.all():
            # understand wich it will be the status of the mocked game
            # 0 => not checkedin,
            # 1 => available
            # 2 => on the table
            # 3 => checkedout
            mode = random.randint(0, 99)
            # mode = random.choice(statuses)

            if 0 <= mode < 5:
                game.location = None
                game.date_checkout = None

            elif 5 <= mode < 85:
                game.location = random.choice(shelves)
                withdraw_filter = game.withdraw_set.filter(date_returned=None)
                if withdraw_filter.count() > 0:
                    for w in withdraw_filter:
                        w.date_returned = timezone.now()
                        w.save()

            elif 85 <= mode < 99:
                game.location = random.choice(shelves)
                withdraw = Withdraw()
                withdraw.game = game
                withdraw.requisitor = random.choice(User.objects.all())
                withdraw.date_withdrawn = timezone.now()
                withdraw.save()

            elif mode >= 7:
                game.location = None
                game.date_checkout = timezone.now()

            game.save()
