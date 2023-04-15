from love_letter.models import Game
from love_letter.repository import create_default_repository
from love_letter.usecase.create_game import CreateGame
from love_letter.usecase.join_game import JoinGame
from love_letter.usecase.play_card import PlayCard
from love_letter.usecase.start_game import StartGame

game_repository = create_default_repository()


class GetStatusInput:
    game_id: str
    player_id: str


class GetStatusOutput:
    game: Game


class GetStatus:
    @classmethod
    def output(cls) -> GetStatusOutput:
        return GetStatusOutput()

    @classmethod
    def input(cls, game_id: str, player_id: str) -> GetStatusInput:
        input = GetStatusInput()
        input.game_id = game_id
        input.player_id = player_id
        return input

    def execute(self, input: GetStatusInput, output: GetStatusOutput):
        game: Game = game_repository.get(input.game_id)
        if game is None:
            output.game = None
            return
        output.game = game
