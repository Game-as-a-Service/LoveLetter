import abc
import logging
import os
import os.path
import pickle
import tempfile
import uuid
from typing import Dict

from love_letter.models import Game

logger = logging.getLogger("repository")
logger.level = logging.INFO
logger.addHandler(logging.StreamHandler())


class GameRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def save_or_update(self, game: Game) -> str:
        # TODO: Should return game id.
        pass

    @abc.abstractmethod
    def get(self, game_id) -> Game:
        pass


class GameRepositoryPickleImpl(GameRepository):
    def __init__(self):
        self.working_dir = tempfile.mkdtemp()
        logger.info(f"{GameRepositoryPickleImpl.__name__} {self.working_dir=}")

    def save_or_update(self, game: Game) -> str:
        if not game.id:
            game.id = uuid.uuid4().hex

        target = os.path.join(self.working_dir, game.id)
        with open(target, "wb") as fh:
            pickle.dump(game, fh)

        return game.id

    def get(self, game_id) -> Game:
        target = os.path.join(self.working_dir, game_id)
        with open(target, "rb") as fh:
            return pickle.load(fh)


class GameRepositoryInMemoryImpl(GameRepository):
    def __init__(self):
        self.in_memory_data: Dict[str, "Game"] = dict()

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
            raise ValueError(f"Game {game_id} does not exist")
        return game


def create_default_repository():
    if os.environ.get("repository_impl") == "pickle":
        return GameRepositoryPickleImpl()

    return GameRepositoryInMemoryImpl()
