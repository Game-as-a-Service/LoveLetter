import unittest
from fastapi.testclient import TestClient


def _test_client() -> TestClient:
    from love_letter.web.example_api import app
    return TestClient(app)


class ExampleApiTests(unittest.TestCase):

    def setUp(self) -> None:
        self.t: TestClient = _test_client()

    def tearDown(self) -> None:
        self.t.close()

    def test_http_get_read_item(self):
        response = self.t.get("/items/5566").json()
        self.assertEqual(dict(item_id=5566), response)

    def test_http_get_read_item_with_parameters(self):
        response = self.t.get("/items_with_params/give_me_10_secs?needy=c8763&limit=10").json()
        self.assertEqual(
            dict(item_id="give_me_10_secs",
                 limit=10,
                 needy="c8763",
                 skip=0),
            response)

    def test_http_post(self):
        response = self.t.post(
            '/items', json=dict(
                name="say my name",
                price=3.14,
                tax=0.1,
                description="breaking bad")).json()
        self.assertEqual(dict(
            name="say my name",
            price=3.14,
            tax=0.1,
            description="breaking bad"), response)

    def test_http_post_with_response_model(self):
        response = self.t.post("/user", json=dict(
            username="9527",
            email="3345678@foobarbar.com",
            full_name="full_name",
            password="你看不到我")).json()

        # response will not contain the password
        self.assertEqual(dict(
            username="9527",
            email="3345678@foobarbar.com",
            full_name="full_name"), response)
