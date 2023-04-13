import traceback
from typing import Dict, Union

from love_letter.models import Game, GuessCard, Player, ToSomeoneCard
from love_letter.repository import create_default_repository
from love_letter.usecase.create_game import CreateGame
from love_letter.usecase.join_game import JoinGame

game_repository = create_default_repository()


class StartGameInput:
    game_id: str


class StartGameOutput:
    success: bool


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
