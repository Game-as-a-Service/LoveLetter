from dataclasses import dataclass

from love_letter.models import Game
from love_letter.models.event import DomainEvent
from love_letter.usecase.common import Presenter, game_repository


class StartGameInput:
    game_id: str


@dataclass
class StartGameEvent(DomainEvent):
    success: bool


class StartGamePresenter(Presenter):
    def as_view_model(self):
        for event in self.events:
            if isinstance(event, StartGameEvent):
                return event.success
        raise BaseException("Game is unavailable.")


class StartGame:
    def execute(self, input: StartGameInput, presenter: Presenter):
        game: Game = game_repository.get(input.game_id)
        if game is None:
            presenter.present([StartGameEvent(success=False)])
            return

        game.start()
        game_repository.save_or_update(game)
        presenter.present([StartGameEvent(success=True)])

    @classmethod
    def input(cls, game_id) -> StartGameInput:
        input = StartGameInput()
        input.game_id = game_id
        return input

    @classmethod
    def presenter(cls) -> Presenter:
        return StartGamePresenter()
