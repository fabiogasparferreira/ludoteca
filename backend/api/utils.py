import time, json

from boardgamegeek import BGGClient
from boardgamegeek import exceptions as bgg_exceptions

from backend.api.models import BggGame


class BggGameUtils:
    @staticmethod
    def create(bgg_id):
        client = BGGClient()
        game = get_external_game(bgg_id)

        bgg_game = BggGame(bggid=game.id)
        bgg_game = external_game_to_api(external=game, game=bgg_game)
        bgg_game.save()
        return bgg_game

    @staticmethod
    def find(bgg_id):
        return BggGame.objects.filter(pk=bgg_id).first()


def external_game_to_api(external, game):
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
            max_count -= 1
            time.sleep(10)

        except bgg_exceptions.BGGApiError:
            print('[ERROR] API response invalid or not parsed')
            max_count -= 1
            time.sleep(10)

        except bgg_exceptions.BGGApiTimeoutError:
            print('[ERROR] Timeout')
            max_count -= 1
            time.sleep(10)

        except Exception as err:
            print('[ERROR] Exceptio caught getting external game: ' + err)
            max_count -= 1
            time.sleep(10)

    raise Exception
