import abc
import uuid
from typing import Dict

from love_letter.models import Game


class GameRepository(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def save_or_update(self, game: Game) -> str:
        # TODO: Should return game id.
        pass

    @abc.abstractmethod
    def get(self, game_id) -> Game:
        pass


class GameRepositoryInMemoryImpl(GameRepository):

    def __init__(self):
        self.in_memory_data: Dict[str, 'Game'] = dict()

    def save_or_update(self, game: Game) -> str:
        if game.id:
            self.in_memory_data[game.id] = game
        else:
            game.id = uuid.uuid4().hex
            self.in_memory_data[game.id] = game
        return game.id

    def get(self, game_id: str) -> Game:
        game = self.in_memory_data.get(game_id)
        if game is None:
            raise ValueError(f'Game {game_id} does not exist')
        return game
