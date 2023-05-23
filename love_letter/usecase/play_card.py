import traceback
from typing import Union

from love_letter.models import Game, GuessCard, ToSomeoneCard
from love_letter.usecase.common import Presenter, game_repository


class PlayCardInput:
    game_id: str
    player_id: str
    card_name: str
    card_action: Union[GuessCard, ToSomeoneCard, None]


class PlayCard:
    def execute(self, input: PlayCardInput, presenter: Presenter):
        try:
            game: Game = game_repository.get(input.game_id)
            if game is None:
                raise BaseException(f"Game {input.game_id} is unavailable.")

            event = game.play(input.player_id, input.card_name, input.card_action)
            game_repository.save_or_update(game)
            presenter.present(event)
        except BaseException as exception:
            traceback.print_exception(exception)

    @classmethod
    def input(
        cls,
        game_id: str,
        player_id: str,
        card_name: str,
        card_action: Union[GuessCard, ToSomeoneCard, None],
    ) -> PlayCardInput:
        input = PlayCardInput()
        input.game_id = game_id
        input.player_id = player_id
        input.card_name = card_name
        input.card_action = card_action
        return input
