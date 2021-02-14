import time

from boardgamegeek import BGGClient
from boardgamegeek import exceptions as bgg_exceptions
from django.contrib.auth import get_user_model

from backend.api.models import BggGame, LibraryGame

User = get_user_model()

class Player:
    @staticmethod
    def create_player(username):
        player = User()
        player.username = username
        player.email = username + '@' + 'dumbmail.com'
        player.first_name = username
        player.save()
        return player


class Library:
    @staticmethod
    def create(bgg_id, owner):
        search = BggGame.objects.filter(bggid=bgg_id)
        if search.count():
            bgg_game = search.first()
        else:

            response = BoardGameGeek.get_external_game(bgg_id)

            bgg_game = BGGGame.create(response.id)

        if bgg_game:
            playersfilter = User.objects.filter(username=owner)

            if playersfilter.count():
                player = playersfilter.first()
            else:
                player = Player.create_player(owner)

            game = LibraryGame(game=bgg_game, owner=player)

            game.game = bgg_game

            game.save()
        else:
            print('game not found (' + str(bgg_id) + ')')


class BGGGame:
    @staticmethod
    def create(bgg_id):
        client = BGGClient()
        game = BoardGameGeek.get_external_game(bgg_id)

        bgg_game = BggGame(bggid=game.id)
        bgg_game = BoardGameGeek.convert_external_game(external=game, game=bgg_game)
        bgg_game.save()
        return bgg_game

    @staticmethod
    def find(bgg_id):
        return BggGame.objects.filter(pk=bgg_id).first()


class BoardGameGeek:
    @staticmethod
    def convert_external_game(external, game):
        game.name = external.name
        game.thumbnail = external.thumbnail or ""
        game.image = external.image or ""
        game.min_players = external.minplayers
        game.max_players = external.maxplayers
        game.min_playtime = external.minplaytime
        game.max_playtime = external.maxplaytime
        game.rank = external.boardgame_rank
        game.other_names = external.alternative_names
        return game

    @staticmethod
    def get_external_game(bgg_id):
        bgg = BGGClient()
        max_count = 10
        while max_count:
            try:
                return bgg.game(game_id=bgg_id)

            except bgg_exceptions.BGGValueError:
                print('[ERROR] Invalid parameters')
                raise

            except bgg_exceptions.BGGApiRetryError:
                print('[ERROR] Retry after delay, retrying...')
                BoardGameGeek._retry(max_count)

            except bgg_exceptions.BGGApiError:
                print('[ERROR] API response invalid or not parsed')
                BoardGameGeek._retry(max_count)

            except bgg_exceptions.BGGApiTimeoutError:
                print('[ERROR] Timeout')
                BoardGameGeek._retry(max_count)

            except Exception as err:
                print('[ERROR] Exception caught getting external game: ' + str(err))
                BoardGameGeek._retry(max_count)

        raise Exception

    @staticmethod
    def _retry(count):
        count -= 1
        time.sleep(1)
