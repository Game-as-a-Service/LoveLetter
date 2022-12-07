import unittest

from starlette.testclient import TestClient

from love_letter.models import Deck
from love_letter.web.app import app


class TestDeck(Deck):
    def shuffle(self, player_num: int):
        super().shuffle(player_num)
        from love_letter.models import find_card_by_name as c

        self.cards = [
            c('侍女'),  # player-a 的初始手牌
            c('神父'),  # player-b 的初始手牌
            c('公主'),  # player-a 為 turn player 獲得的牌
            c('衛兵'),
            c('伯爵夫人'),
            c('衛兵'),
        ]


class LostHandMaidProtected(unittest.TestCase):
    def setUp(self) -> None:
        self.t = TestClient(app)

    def tearDown(self) -> None:
        self.t.close()

    def test_finish_one_round_lose_handmaid_protected(self):
        game_id = "g-5566"

        # 將牌庫換成測試用牌庫
        import love_letter.models
        love_letter.models.deck_factory = lambda: TestDeck()

        # 開始遊戲
        response = self.t.post(f"/games/{game_id}/start").json()
        self.assertEqual(dict(
            game_id=game_id,
            players=[dict(name="player-a", out=False), dict(name="player-b", out=False)],
            rounds=[
                dict(
                    winner=None,
                    players=[dict(name="player-a", out=False), dict(name="player-b", out=False)]
                )
            ]
        ), response)

        # 玩家A 出牌 獲得侍女保護
        response = self.t.post(f"/games/{game_id}/player/player-a/card/侍女/play").json()
        self.assertEqual(dict(
            game_id=game_id,
            players=[dict(name="player-a", out=False), dict(name="player-b", out=False)],
            rounds=[
                dict(
                    winner=None,
                    players=[dict(name="player-a", out=False), dict(name="player-b", out=False)]
                )
            ]
        ), response)

        # 玩家B 對 玩家A 出牌 衛兵 指定 公主 => 玩家A 被侍女保護 無效
        request_body = {
            "chosen_player": "player-a",
            "guess_card": "公主"
        }
        response = self.t.post(f"/games/{game_id}/player/player-b/card/衛兵/play", json=request_body).json()
        self.assertEqual(dict(
            game_id=game_id,
            players=[dict(name="player-a", out=False), dict(name="player-b", out=False)],
            rounds=[
                dict(
                    winner=None,
                    players=[dict(name="player-a", out=False), dict(name="player-b", out=False)]
                )
            ]
        ), response)

        # 玩家A 出牌 伯爵夫人
        response = self.t.post(f"/games/{game_id}/player/player-a/card/伯爵夫人/play").json()
        self.assertEqual(dict(
            game_id=game_id,
            players=[dict(name="player-a", out=False), dict(name="player-b", out=False)],
            rounds=[
                dict(
                    winner=None,
                    players=[dict(name="player-a", out=False), dict(name="player-b", out=False)]
                )
            ]
        ), response)

        # 玩家B 對 玩家A 出牌 衛兵 指定 公主 => 玩家A 出局
        request_body = {
            "chosen_player": "player-a",
            "guess_card": "公主"
        }
        response = self.t.post(f"/games/{game_id}/player/player-b/card/衛兵/play", json=request_body).json()
        self.assertEqual(dict(
            game_id=game_id,
            players=[dict(name="player-a", out=False), dict(name="player-b", out=False)],
            rounds=[
                dict(
                    winner="player-b",
                    players=[dict(name="player-a", out=True), dict(name="player-b", out=False)]
                ),
                dict(
                    winner=None,
                    players=[dict(name="player-a", out=False), dict(name="player-b", out=False)]
                )
            ]
        ), response)
