import traceback
from typing import Dict, Union

from love_letter.models import Game, GuessCard, Player, ToSomeoneCard
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


class PlayCardInput:
    game_id: str
    player_id: str
    card_name: str
    card_action: Union[GuessCard, ToSomeoneCard, None]


class PlayCardOutput:
    game: Game


class PlayCard:
    @classmethod
    def output(cls) -> PlayCardOutput:
        return PlayCardOutput()

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

    def execute(self, input: PlayCardInput, output: PlayCardOutput):
        game: Game = game_repository.get(input.game_id)
        if game is None:
            output.game = None
            return

        game.play(input.player_id, input.card_name, input.card_action)
        game_repository.save_or_update(game)
        output.game = game


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
