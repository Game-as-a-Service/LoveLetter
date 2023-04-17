from dataclasses import dataclass

from love_letter.models import Game
from love_letter.models.event import DomainEvent
from love_letter.usecase.common import Presenter, game_repository


class GetStatusInput:
    game_id: str
    player_id: str


@dataclass
class GetStatusEvent(DomainEvent):
    game: Game


class GetStatusPresenter(Presenter):
    def as_view_model(self) -> Game:
        for event in self.events:
            if isinstance(event, GetStatusEvent):
                return event.game
        raise BaseException("Game is unavailable.")


class GetStatus:
    def execute(self, input: GetStatusInput, presenter: Presenter):
        game: Game = game_repository.get(input.game_id)
        presenter.present(events=[GetStatusEvent(game)])

    @classmethod
    def input(cls, game_id: str, player_id: str) -> GetStatusInput:
        input = GetStatusInput()
        input.game_id = game_id
        input.player_id = player_id
        return input

    @classmethod
    def presenter(cls) -> "GetStatusPresenter":
        return GetStatusPresenter()
