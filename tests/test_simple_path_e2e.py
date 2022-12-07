import json
import unittest
from fastapi.testclient import TestClient

from love_letter.models import Deck


def _test_client() -> TestClient:
    from love_letter.web.app import app
    return TestClient(app)


class TestDeck(Deck):

    def shuffle(self, player_num: int):
        super().shuffle(player_num)
        from love_letter.models import find_card_by_name as c

        self.cards = [
            c('衛兵'),  # player-a 的初始手牌
            c('神父'),  # player-b 的初始手牌
            c('公主'),  # player-a 為 turn player 獲得的牌
            c('衛兵')
        ]


class LoveLetterSimpleCaseEndToEndTests(unittest.TestCase):

    def setUp(self) -> None:
        self.t: TestClient = _test_client()

    def tearDown(self) -> None:
        self.t.close()

    def test_start_game_with_predefined_state(self):
        game_id = "g-5566"

        # 將牌庫換成測試用牌庫
        import love_letter.models
        love_letter.models.deck_factory = lambda: TestDeck()

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
            "chosen_player": "player-b",
            "guess_card": "神父"
        }
        response = self.t.post(f"/games/{game_id}/player/player-a/card/衛兵/play", json=request_body).json()
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
