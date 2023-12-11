import abc
import logging
import os
import os.path
import pickle
import tempfile
from typing import Dict

from pymongo import MongoClient
from pymongo.collection import Collection

from love_letter.config import config
from love_letter.models import Game
from love_letter.repository.data import GameData

logger = logging.getLogger("repository")
logger.level = logging.INFO
logger.addHandler(logging.StreamHandler())


class GameRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def save_or_update(self, game: Game):
        pass

    @abc.abstractmethod
    def get(self, game_id) -> Game:
        pass


class GameRepositoryPickleImpl(GameRepository):
    def __init__(self):
        self.working_dir = tempfile.mkdtemp()
        logger.info(f"{GameRepositoryPickleImpl.__name__} {self.working_dir=}")

    def save_or_update(self, game: Game):
        target = os.path.join(self.working_dir, game.id)
        with open(target, "wb") as fh:
            pickle.dump(game, fh)

    def get(self, game_id) -> Game:
        target = os.path.join(self.working_dir, game_id)
        with open(target, "rb") as fh:
            return pickle.load(fh)


class GameRepositoryInMemoryImpl(GameRepository):
    def __init__(self):
        self.in_memory_data: Dict[str, "Game"] = dict()

    def save_or_update(self, game: Game):
        self.in_memory_data[game.id] = game

    def get(self, game_id: str) -> Game:
        game = self.in_memory_data.get(game_id)
        if game is None:
            raise ValueError(f"Game {game_id} does not exist")
        return game


class GameRepositoryMongoDBImpl(GameRepository):
    def __init__(self):
        self.collection: Collection = (
            MongoClient(config.DB_HOST, config.DB_PORT)
            .get_database(config.DB_NAME)
            .get_collection(config.DB_COLLECTION)
        )

    def save_or_update(self, game: Game):
        game = GameData.to_dict(game)
        find_filter = {"game_id": game["game_id"]}
        update_filter = {"$set": game}

        _find = list(self.collection.find(find_filter))
        if _find:
            self.collection.update_one(find_filter, update_filter)
        else:
            self.collection.insert_one(game)

    def get(self, game_id: str) -> Game:
        game: Dict = next(self.collection.find({"game_id": game_id}))
        if game is None:
            raise ValueError(f"Game {game_id} does not exist")
        return GameData.to_domain(game)


_created_game_repo = None


def create_default_repository():
    global _created_game_repo

    if _created_game_repo is not None:
        return _created_game_repo

    if config.REPOSITORY_IMPL == "pickle":
        _created_game_repo = GameRepositoryPickleImpl()
        return _created_game_repo
    elif config.REPOSITORY_IMPL == "mongo":
        _created_game_repo = GameRepositoryMongoDBImpl()
        return _created_game_repo

    _created_game_repo = GameRepositoryInMemoryImpl()
    return _created_game_repo
