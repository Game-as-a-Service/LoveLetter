import traceback
from dataclasses import dataclass

from love_letter.models import Player
from love_letter.models.event import DomainEvent
from love_letter.usecase.common import Presenter, game_repository


class PlayerJoinGameInput:
    game_id: str
    player_id: str


@dataclass
class PlayerJoinedEvent(DomainEvent):
    success: bool


class JoinGamePresenter(Presenter):
    def as_view_model(self):
        for event in self.events:
            if isinstance(event, PlayerJoinedEvent):
                return event.success
        raise BaseException("Game is unavailable.")


class JoinGame:
    def execute(self, input: PlayerJoinGameInput, presenter: JoinGamePresenter):
        try:
            game = game_repository.get(input.game_id)
            game.join(Player(input.player_id))
            game_repository.save_or_update(game)
            presenter.present([PlayerJoinedEvent(success=True)])
        except BaseException as e:
            traceback.print_exception(e)
            presenter.present([PlayerJoinedEvent(success=False)])

    @classmethod
    def input(cls, game_id: str, player_id: str) -> PlayerJoinGameInput:
        input = PlayerJoinGameInput()
        input.game_id = game_id
        input.player_id = player_id
        return input

    @classmethod
    def presenter(cls) -> JoinGamePresenter:
        return JoinGamePresenter()
