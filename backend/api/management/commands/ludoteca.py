from _ast import keyword

import pandas as pd
from boardgamegeek import BGGClient
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from backend.api import utils
from backend.api.models import Location, Configuration

User = get_user_model()

bgg = BGGClient()


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('file')

    def add_game(self, bggid, owners):
        for owner in owners:
            utils.Library.create(bggid, owner.strip())

    #@transaction.atomic
    def handle(self, *args, **options):
        print('------------------------------------')
        print('-- ludoteca dummy data generation --')
        print('------------------------------------')
        # create locations
        # TODO: Move this to a config file

        print('[1/3] Create locations')
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

        print('[2/3] Create library games')
        # load library from file
        skipped = []
        self.stdout.write(options['file'])
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

        print('[3/3] Create default configurations')
        conf = Configuration()
        conf.key = 'convention_user'
        conf.type = Configuration.Types.LIBRARY
        conf.save()
        conf = Configuration()
        conf.key = 'associate_discount'
        conf.type = Configuration.Types.STORE
        conf.value = '0'
        conf.save()
