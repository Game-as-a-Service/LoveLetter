import os
from unittest import TestCase

from pymongo import MongoClient
from testcontainers.mongodb import MongoDbContainer

from tests.test_game_service import GameServiceTests

os.environ["repository_impl"] = "mongo"


class MongoTestCase(TestCase):
    mongo_container: MongoDbContainer = None

    @classmethod
    def setUpClass(cls):
        """Start a MongoDB container for testing."""
        super().setUpClass()

        # Start the MongoDB container
        cls.mongo_container = MongoDbContainer()
        cls.mongo_container.start()

        # Create the MongoDB client
        cls.client = MongoClient(
            cls.mongo_container.get_container_host_ip(),
            int(cls.mongo_container.get_exposed_port(27017)),
            username="test",
            password="test",
        )

    @classmethod
    def tearDownClass(cls):
        """Stop and remove the MongoDB container."""
        super().tearDownClass()

        # Stop and remove the container
        cls.mongo_container.stop()

    def setUp(self):
        """Set up test-specific resources."""
        super().setUp()

        # Create a new database for each test
        self.db = self.client["test_db"]

    def tearDown(self):
        """Clean up test-specific resources."""
        super().tearDown()

        # Drop the test database after each test
        self.client.drop_database("test_db")


class MyMongoTest(MongoTestCase, GameServiceTests):
    def test_use_client_example(self):
        """Test inserting data into MongoDB."""

        # Insert a document into a test collection
        collection = self.db["test_collection"]
        document = {"name": "John Doe", "email": "johndoe@example.com"}
        result = collection.insert_one(document)

        # Assert that the document was inserted successfully
        self.assertTrue(result.acknowledged)
        self.assertIsNotNone(result.inserted_id)

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


# collection = MongoClient('192.168.223.127', 27017).get_database("test_db").get_collection("test_collection")
# print(type(db))
# db = client["test_db"]
# collection = db["test_collection"]
# document = {"name": "John Doe", "email": "johndoe@example.com"}
# result = collection.insert_one(document)
# print(result.acknowledged)
# print(result.inserted_id)

# result = collection.find({"name": "John Doe"})
# print(list(result))

# result = collection.update_one(, upsert=True)
# print(result)

# data = {"name": "eddy", "email": "aaa"}
# _find = next(collection.find({"name": data["name"]}))
# print(_find)
# if _find:
#     new_data = {"name": "eddy", "email": "bbbb"}
#     collection.update_one({"_id": _find["_id"]}, {"$set": new_data})
# else:
#     collection.insert_one(data)
