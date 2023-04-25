from love_letter.models import Game, Player
from love_letter.usecase.common import Presenter, game_repository


class CreateGameInput:
    player_id: str


class CreateGame:
    def execute(self, input: CreateGameInput, presenter: Presenter):
        game = Game()
        events = game.join(Player(input.player_id))
        game_repository.save_or_update(game)
        presenter.present([events])

    @classmethod
    def input(cls, player_id: str) -> CreateGameInput:
        input = CreateGameInput()
        input.player_id = player_id
        return input
