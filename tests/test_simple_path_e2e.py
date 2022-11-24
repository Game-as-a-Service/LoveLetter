import json
import unittest
from fastapi.testclient import TestClient


def _test_client() -> TestClient:
    from love_letter.web.app import app
    return TestClient(app)


class LoveLetterSimpleCaseEndToEndTests(unittest.TestCase):

    def setUp(self) -> None:
        self.t: TestClient = _test_client()

    def tearDown(self) -> None:
        self.t.close()

    def test_start_game_with_predefined_state(self):
        game_id = "g-5566"

        # 開始遊戲
        response = self.t.post(f"/games/{game_id}/start").json()
        self.assertEqual(dict(
            game_id="g-5566",
            players=[dict(name="player-a", out=False), dict(name="player-b", out=False)],
            rounds=[
                dict(
                    winner=None,
                    players=[dict(name="player-a", out=False), dict(name="player-b", out=False)]
                )
            ]
        ), response)

        # 玩家出牌
        request_body = {
            "turn_player": "player-a",
            "opponent": "player-b",
            "card_action": [
                1,
                2
            ]
        }
        response = self.t.post(f"/games/{game_id}/play", json=request_body).json()
        self.assertEqual(dict(
            game_id="g-5566",
            players=[dict(name="player-a", out=False), dict(name="player-b", out=False)],
            rounds=[
                dict(
                    winner="player-a",
                    players=[dict(name="player-a", out=False), dict(name="player-b", out=True)]
                ),
                dict(
                    winner=None,
                    players=[dict(name="player-a", out=False), dict(name="player-b", out=False)]
                )
            ]
        ), response)

        print(json.dumps(response))
