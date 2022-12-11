import traceback
from typing import Dict, Optional, Union

from love_letter.models import Game, Player
from love_letter.repository import GameRepository
from love_letter.web.dto import GuessCard, ToSomeoneCard


class GameService:

    def __init__(self, repository: GameRepository):
        self.repository = repository

    def create_game(self, player_id: str) -> str:
        game = Game()
        # TODO for now, we dont have the registration process,
        # TODO just create the player when they are creating or joining the game
        game.join(Player.create(player_id))
        return self.repository.save_or_update(game)

    def join_game(self, game_id: str, player_id: str) -> bool:
        try:
            self.repository.get(game_id).join(Player.create(player_id))
            return True
        except BaseException as e:
            traceback.print_exception(e)
            return False

    def start_game(self, game_id: str) -> Optional[Dict]:
        game: Game = self.repository.get(game_id)
        if game is None:
            return
        game.start()
        return game.to_dict()

    def play_card(self, game_id, player_id: str, card_name: str,
                  card_action: Union[GuessCard, ToSomeoneCard, None]) -> Optional[Dict]:

        game: Game = self.repository.get(game_id)
        if game is None:
            return
        game.play(player_id, card_name, card_action)
        return game.to_dict()
