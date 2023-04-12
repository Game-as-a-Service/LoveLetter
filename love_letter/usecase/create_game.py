from dataclasses import dataclass

from love_letter.models import Game, Player
from love_letter.models.event import DomainEvent
from love_letter.usecase.common import Presenter, game_repository


class CreateGameInput:
    player_id: str


@dataclass
class GameCreatedEvent(DomainEvent):
    game_id: str


class CreateGamePresenter(Presenter):
    def as_view_model(self):
        for event in self.events:
            if isinstance(event, GameCreatedEvent):
                return event.game_id


class CreateGame:
    def execute(self, input: CreateGameInput, presenter: Presenter):
        game = Game()
        game.join(Player(input.player_id))
        game_id = game_repository.save_or_update(game)
        presenter.present([GameCreatedEvent(game_id=game_id)])

    @classmethod
    def input(cls, player_id: str) -> CreateGameInput:
        input = CreateGameInput()
        input.player_id = player_id
        return input

    @classmethod
    def presenter(cls) -> CreateGamePresenter:
        return CreateGamePresenter()
