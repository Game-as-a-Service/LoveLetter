import traceback

from love_letter.models import Game, Player
from love_letter.repository import create_default_repository

game_repository = create_default_repository()


class CreateGameInput:
    player_id: str


class CreateGameOutput:
    game_id: str


class CreateGame:
    def execute(self, input: CreateGameInput, output: CreateGameOutput):
        game = Game()
        game.join(Player(input.player_id))
        game_id = game_repository.save_or_update(game)
        output.game_id = game_id

    @classmethod
    def input(cls, player_id: str) -> CreateGameInput:
        input = CreateGameInput()
        input.player_id = player_id
        return input

    @classmethod
    def output(cls) -> CreateGameOutput:
        return CreateGameOutput()


class JoinGameInput:
    game_id: str
    player_id: str


class JoinGameOutput:
    success: bool


class JoinGame:
    def execute(self, input: JoinGameInput, output: JoinGameOutput):
        try:
            game = game_repository.get(input.game_id)
            game.join(Player(input.player_id))
            game_repository.save_or_update(game)
            output.success = True
        except BaseException as e:
            traceback.print_exception(e)
            output.success = False

    @classmethod
    def output(cls) -> JoinGameOutput:
        output = JoinGameOutput()
        return output

    @classmethod
    def input(cls, game_id: str, player_id: str) -> JoinGameInput:
        input = JoinGameInput()
        input.game_id = game_id
        input.player_id = player_id
        return input


class StartGameInput:
    game_id: str


class StartGameOutput:
    success: bool

    pass


class StartGame:
    @classmethod
    def output(cls) -> StartGameOutput:
        return StartGameOutput()

    @classmethod
    def input(cls, game_id) -> StartGameInput:
        input = StartGameInput()
        input.game_id = game_id
        return input

    def execute(self, input: StartGameInput, output: StartGameOutput):
        game: Game = game_repository.get(input.game_id)
        if game is None:
            output.success = False
            return

        game.start()
        game_repository.save_or_update(game)
        output.success = True
