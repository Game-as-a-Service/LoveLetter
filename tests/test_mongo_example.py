import unittest

from pymongo import MongoClient
from testcontainers.mongodb import MongoDbContainer

import love_letter.repository
from love_letter import config
from love_letter.repository import GameRepositoryMongoDBImpl
from tests.test_game_service import GameServiceTests, PlayerContextTest


class GameRepositoryMongoTestDBImpl(GameRepositoryMongoDBImpl):
    def __init__(self):
        super(GameRepositoryMongoTestDBImpl, self).__init__()
        # Start the MongoDB container
        self.mongo_container = MongoDbContainer()
        self.mongo_container.start()

        # Create the MongoDB client
        self.client = MongoClient(
            self.mongo_container.get_container_host_ip(),
            int(self.mongo_container.get_exposed_port(27017)),
            username="test",
            password="test",
        )
        self.db = self.client["test_db"]
        self.collection = self.db["test_collection"]


love_letter.repository.get_mongo_impl = lambda: GameRepositoryMongoTestDBImpl()


@unittest.skipIf(config.REPOSITORY_IMPL != "mongo", "Just run on mongo repository")
class MyMongoTest(GameServiceTests, PlayerContextTest):
    pass

    # def test_use_client_example(self):
    #     """Test inserting data into MongoDB."""
    #
    #     # Insert a document into a test collection
    #     collection = self.db["test_collection"]
    #     document = {"name": "John Doe", "email": "johndoe@example.com"}
    #     result = collection.insert_one(document)
    #
    #     # Assert that the document was inserted successfully
    #     self.assertTrue(result.acknowledged)
    #     self.assertIsNotNone(result.inserted_id)

    # def test_use_with_example(self):
    #     with MongoDbContainer("mongo:latest") as mongo:
    #         db = mongo.get_connection_client().test
    #         # Insert a database entry
    #         result = db.restaurants.insert_one({"name": "John Doe", "email": "johndoe@example.com"})
    #
    #         print(result.acknowledged)
    #         print(result.inserted_id)
    #         cursor = db.restaurants.find({"name": "John Doe"})
    #         print(list(cursor))
