import traceback
from typing import Dict, Optional, Union, List, Any

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

        # Set previous round players cards can_discard=False、choose_players=[]
        if len(raw_result['rounds']) > 1:
            for round in raw_result['rounds'][:-1]:
                for p in round['players']:
                    self._add_cards_usage(p, None, None, True)
                self._add_cards_usage(round['turn_player'], None, None, True)

        last_round = raw_result['rounds'][-1]
        last_round_alive_players = [p['name'] for p in last_round['players'] if not p['out']]
        turn_player = last_round['turn_player']

        for p in last_round['players']:
            if p['name'] != player_id:
                p['cards'] = []
            else:
                self._add_cards_usage(p, turn_player, last_round_alive_players)

        if turn_player['name'] != player_id:
            turn_player['cards'] = []
        else:
            self._add_cards_usage(turn_player, turn_player, last_round_alive_players)

        return raw_result

    def _add_cards_usage(
            self,
            player: Dict[str, Any],
            turn_player: Optional[Dict[str, Any]],
            last_round_alive_players: Optional[List[str]],
            previous_round: bool = False
    ):
        """
        Add turn_player cards usage.
        :param player:
        :param turn_player:
        :param last_round_alive_players:
        :param previous_round:
        :return:
        """
        hand_cards = [c['name'] for c in player['cards']]
        for c in player['cards']:
            # if is previous_round = True set 'can_discard'、'choose_players' to default value
            if previous_round:
                c['can_discard'] = False
                c['choose_players'] = []
                continue

            # if the player is not turn_player all cards can't be discarded
            if player['name'] != turn_player['name']:
                c['can_discard'] = False
            else:
                c['can_discard'] = c['can_discard'](hand_cards)

            # if the player is turn_player all cards can be discarded，and have choose_players value
            if c['can_discard']:
                c['choose_players'] = c['choose_players'](player['name'], last_round_alive_players)
            else:
                c['choose_players'] = []
