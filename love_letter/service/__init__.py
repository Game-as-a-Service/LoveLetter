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

    def start_game(self, game_id: str) -> bool:
        game: Game = self.repository.get(game_id)
        if game is None:
            return
        game.start()
        return True

    def play_card(self, game_id, player_id: str, card_name: str,
                  card_action: Union[GuessCard, ToSomeoneCard, None]) -> Optional[Dict]:

        game: Game = self.repository.get(game_id)
        if game is None:
            return
        game.play(player_id, card_name, card_action)
        return self._convert_to_player_view(game, player_id)

    def get_status(self, game_id: str, player_id: str):
        game: Game = self.repository.get(game_id)
        if game is None:
            return

        return self._convert_to_player_view(game, player_id)

    def _convert_to_player_view(self, game, player_id):
        # we should remove private data for each player
        # players only know their own cards
        raw_result = game.to_dict()
        if len(raw_result['rounds']) < 1:
            return raw_result

        last_round = raw_result['rounds'][-1]
        for p in last_round['players']:
            if p['name'] != player_id:
                p['cards'] = []
            self._add_cards_usage(p)

        turn_player = last_round['turn_player']
        if turn_player['name'] != player_id:
            turn_player['cards'] = []
        else:
            self._add_cards_usage(turn_player)

        return raw_result

    def _add_cards_usage(self, turn_player):
        hand_cards = [c["name"] for c in turn_player["cards"]]
        for c in turn_player['cards']:
            c['can_discard'] = c['can_discard'](hand_cards)
