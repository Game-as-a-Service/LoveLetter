from love_letter.config import FRONTEND_HOST
from love_letter.models import Game, Player
from love_letter.models.event import GameEvent
from love_letter.usecase.common import Presenter, game_repository


class LobbyStartGame:
    def execute(self, input: "LobbyPlayers", presenter: Presenter):
        game = Game()
        for player in input.players:
            game.join(Player(player.nickname, player.id))
        game.start()
        game_repository.save_or_update(game)
        presenter.present([GameEvent(url=f"{FRONTEND_HOST}/games/{game.id}")])
