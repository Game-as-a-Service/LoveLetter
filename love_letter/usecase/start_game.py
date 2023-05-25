from love_letter.models import Game, GameException
from love_letter.usecase.common import Presenter, game_repository


class StartGameInput:
    game_id: str


class StartGame:
    def execute(self, input: StartGameInput, presenter: Presenter):
        game: Game = game_repository.get(input.game_id)
        if game is None:
            raise GameException("No such game")

        events = game.start()
        game_repository.save_or_update(game)
        presenter.present(events)

    @classmethod
    def input(cls, game_id) -> StartGameInput:
        input = StartGameInput()
        input.game_id = game_id
        return input
