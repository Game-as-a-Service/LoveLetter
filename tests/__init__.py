import unittest
from typing import Optional

from pymongo.database import Database
from testcontainers.mongodb import MongoDbContainer

from love_letter.repository import GameRepositoryMongoDBImpl
from love_letter.repository import create_default_repository


class LoveLetterRepositoryAwareTestCase(unittest.TestCase):
    test_container: Optional[MongoDbContainer]

    @classmethod
    def setUpClass(cls):
        repo = create_default_repository()
        if isinstance(repo, GameRepositoryMongoDBImpl):
            cls.test_container = MongoDbContainer("mongo:latest")
            cls.test_container.start()

            from pymongo import MongoClient
            from pymongo.collection import Collection

            db: MongoClient = cls.test_container.get_connection_client()
            repo.collection: Collection = db.get_database("love_letter").get_collection(
                "love_letter"
            )
            print("override the mongo-collection: ", repo.collection)

    @classmethod
    def tearDownClass(cls):
        if isinstance(create_default_repository(), GameRepositoryMongoDBImpl):
            cls.test_container.stop()
