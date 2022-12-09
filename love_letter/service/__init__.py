from typing import Dict, Optional, Union

from love_letter.models import Game, Player
from love_letter.web.dto import GuessCard, ToSomeoneCard

database = dict()


def build_fake_data():
    global database

    game = Game()
    game.id = 'g-5566'
    database['g-5566'] = game

    player_a = Player()
    player_a.name = 'player-a'
    player_a.cards = []
    game.join(player_a)

    player_b = Player()
    player_b.name = 'player-b'
    player_b.cards = []
    game.join(player_b)


build_fake_data()


class GameService:
    def start_game(self, game_id: str) -> Optional[Dict]:
        if game_id not in database:
            return
        game: Game = database.get(game_id)
        game.start()
        return game.to_dict()

    def play_card(self, game_id, player_id: str, card_name: str,
                  card_action: Union[GuessCard, ToSomeoneCard, None]) -> Optional[Dict]:
        if game_id in database:
            game: Game = database.get(game_id)
            game.play(player_id, card_name, card_action)
            return game.to_dict()
        return
