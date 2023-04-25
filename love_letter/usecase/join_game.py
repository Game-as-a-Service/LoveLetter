import traceback

from love_letter.models import Player
from love_letter.usecase.common import Presenter, game_repository


class PlayerJoinGameInput:
    game_id: str
    player_id: str


class JoinGame:
    def execute(self, input: PlayerJoinGameInput, presenter: Presenter):
        try:
            game = game_repository.get(input.game_id)
            events = game.join(Player(input.player_id))
            game_repository.save_or_update(game)
            presenter.present([events])
        except BaseException as e:
            traceback.print_exception(e)
            presenter.present(list(e.args))

    @classmethod
    def input(cls, game_id: str, player_id: str) -> PlayerJoinGameInput:
        input = PlayerJoinGameInput()
        input.game_id = game_id
        input.player_id = player_id
        return input
