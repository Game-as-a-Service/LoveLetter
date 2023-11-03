from love_letter.models import Game
from love_letter.models.event import GetStatusEvent
from love_letter.usecase.common import Presenter, game_repository


class LobbyGameStatusInput:
    game_id: str
    player_id: str


class LobbyGameStatus:
    def execute(self, input: LobbyGameStatusInput, presenter: Presenter):
        game: Game = game_repository.get(input.game_id)
        presenter.present(events=[GetStatusEvent(game)])

    @classmethod
    def input(cls, game_id: str, player_id: str) -> LobbyGameStatusInput:
        input = LobbyGameStatusInput()
        input.game_id = game_id
        input.player_id = player_id
        return input
