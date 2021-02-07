import math
import random
import time

import boardgamegeek
import pandas as pd
from boardgamegeek import BGGClient
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from backend.api.models import BggGame, LibraryGame, Location, Withdraw
from backend.api.utils import BggGameUtils

User = get_user_model()

bgg = BGGClient()


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('file')

    def find(self, query):
        max_count = 10
        while max_count:
            try:
                rs = bgg.search(query)

                if rs:
                    return bgg.game(game_id=rs[0].id)

            except boardgamegeek.exceptions.BGGValueError:
                raise

            except boardgamegeek.exceptions.BGGApiRetryError:
                max_count -= 1
                time.sleep(10)

            except boardgamegeek.exceptions.BGGApiError:
                max_count -= 1
                time.sleep(10)

            except boardgamegeek.exceptions.BGGApiTimeoutError:
                max_count -= 1
                time.sleep(10)

            except Exception as err:
                max_count -= 1
                time.sleep(10)

        raise Exception

    def create_bgg(self, game):
        return BggGameUtils.create(game.id)

    def create_player(self, username):
        player = User()
        player.username = username
        player.email = username + '@' + 'dumbmail.com'
        player.first_name = username
        player.save()
        return player

    def add_game(self, bggid, owners):
        for owner in owners:
            self.add_game_to_owner(bggid, owner.strip())

    def add_game_to_owner(self, bggid, owner):
        search = BggGame.objects.filter(bggid=bggid)
        if search.count():
            bgggame = search.first()
        else:

            response = self.find(bggid)

            bgggame = self.create_bgg(response)

        if bgggame:
            playersfilter = User.objects.filter(username=owner)

            if playersfilter.count():
                player = playersfilter.first()
            else:
                player = self.create_player(owner)

            game = LibraryGame(game=bgggame, owner=player)

            game.game = bgggame

            game.save()
        else:
            print('game not found (' + str(bggid) + ')')

    @transaction.atomic
    def handle(self, *args, **options):
        print('------------------------------------')
        print('-- ludoteca dummy data generation --')
        print('------------------------------------')
        # create locations
        # TODO: Move this to a config file

        print('1. Create locations')
        locations = [
            'A1', 'A2', 'A3', 'A4', 'A5',
            'B1', 'B2', 'B3', 'B4', 'B5',
            'C1', 'C2', 'C3', 'C4', 'C5',
            'D1', 'D2', 'D3', 'D4', 'D5',
            'E1', 'E2', 'E3', 'E4', 'E5',
            'leiriakidz'
        ]

        for location in locations:
            location_object = Location()
            location_object.name = location
            location_object.save()

        print('Done')

        # create players
        print('2. Create users')
        # TODO: Move this to a config file
        reader = pd.read_csv('https://my.api.mockaroo.com/players.json?key=5dec1ef0', header=0, delimiter=',')

        User.objects.create_superuser(username='admin', email='admin@example.com', password='admin')

        for _, row in reader.iterrows():
            user = User()
            user.first_name = row['first_name']
            user.last_name = row['last_name']
            user.email = row['email']
            user.username = row['username']
            user.save()

        print('Done')

        print('3. Create library games')
        # load library from file
        skipped = []
        table = pd.read_csv('backend/bgggames_table.csv', header=0, delimiter=';')
        for _, row in table.iterrows():
            bgggame = BggGame()
            bgggame.bggid = row['bggid']
            bgggame.name = row['name']
            bgggame.rank = float(row['rank']) if not math.isnan(float(row['rank'])) else None
            bgggame.min_players = row['min_players']
            bgggame.max_players = row['max_players']
            bgggame.min_playtime = row['min_playtime']
            bgggame.max_playtime = row['max_playtime']
            bgggame.image = row['image']
            bgggame.thumbnail = row['thumbnail']
            bgggame.save()

        table = pd.read_csv(options['file'], header=0, delimiter=';')
        for _, row in table.iterrows():
            owners = row['owners'].split(",")
            bggid = row['bggid']
            if bggid:
                try:
                    self.add_game(bggid, owners)
                except Exception as err:
                    # add to skip file
                    skipped.append(str(bggid) + ';' + row['owners'])

            else:
                print('game without id')

        print(f'Done (number of games skipped: {len(skipped)})')

        print('4. Set library games location and randomize status')
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
        print('Done')
        print('Exiting...')
