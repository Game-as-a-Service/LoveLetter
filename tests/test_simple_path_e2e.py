import unittest

from fastapi.testclient import TestClient

from love_letter.models import Deck, Round
from tests import LoveLetterRepositoryAwareTestCase


def _test_client() -> TestClient:
    from love_letter.web.app import app

    return TestClient(app)


class TestDeckForSimpleE2E(Deck):
    def shuffle(self, player_num: int):
        super().shuffle(player_num)
        from love_letter.models import find_card_by_name as c

        self.cards = [
            c("衛兵"),  # player-a 的初始手牌
            c("神父"),  # player-b 的初始手牌
            c("公主"),  # player-a 為 turn player 獲得的牌
            c("衛兵"),
        ]


class LoveLetterSimpleCaseEndToEndTests(LoveLetterRepositoryAwareTestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.t: TestClient = _test_client()
        # disable random-picker for the first round
        # it always returns the first player
        self.origin_choose_one_randomly = Round.choose_one_randomly
        Round.choose_one_randomly = lambda players: players[0]

    def tearDown(self) -> None:
        Round.choose_one_randomly = self.origin_choose_one_randomly
        self.t.close()

    def test_start_game_with_predefined_state(self):
        player_a = "player-a"
        player_b = "player-b"

        # 將牌庫換成測試用牌庫
        import love_letter.models

        love_letter.models.deck_factory = lambda: TestDeckForSimpleE2E()

        # 建立遊戲
        game_id = self.t.post(f"/games/create/by_player/{player_a}").json()

        # 加入遊戲
        is_success = self.t.post(f"/games/{game_id}/player/{player_b}/join").json()
        self.assertTrue(is_success)

        # 開始遊戲
        is_started = self.t.post(f"/games/{game_id}/start").json()
        self.assertTrue(is_started)

        # 確認遊戲狀態
        response = self.t.get(f"/games/{game_id}/player/{player_a}/status").json()
        self.assertEqual(
            {
                "game_id": game_id,
                "events": [{"type": "round_started", "winner": None}],
                "players": [
                    {"id": None, "name": "player-a", "score": 0},
                    {"id": None, "name": "player-b", "score": 0},
                ],
                "rounds": [
                    {
                        "players": [
                            {
                                "seen_cards": [],
                                "cards": [
                                    {
                                        "description": "猜測一名對手的手牌(不可猜衛兵)，猜測正確對方立刻出局。",
                                        "name": "衛兵",
                                        "value": 1,
                                        "usage": {
                                            "can_discard": True,
                                            "choose_players": ["player-b"],
                                            "can_guess_cards": [
                                                "神父",
                                                "男爵",
                                                "侍女",
                                                "王子",
                                                "國王",
                                                "伯爵夫人",
                                                "公主",
                                            ],
                                        },
                                    },
                                    {
                                        "description": "如果把公主打出在桌面，就會立刻出局。",
                                        "name": "公主",
                                        "value": 8,
                                        "usage": {
                                            "can_discard": True,
                                            "choose_players": [],
                                            "can_guess_cards": [],
                                        },
                                    },
                                ],
                                "name": "player-a",
                                "out": False,
                            },
                            {
                                "cards": [],
                                "seen_cards": [],
                                "name": "player-b",
                                "out": False,
                            },
                        ],
                        "turn_player": {
                            "seen_cards": [],
                            "cards": [
                                {
                                    "description": "猜測一名對手的手牌(不可猜衛兵)，猜測正確對方立刻出局。",
                                    "name": "衛兵",
                                    "value": 1,
                                    "usage": {
                                        "can_discard": True,
                                        "choose_players": ["player-b"],
                                        "can_guess_cards": [
                                            "神父",
                                            "男爵",
                                            "侍女",
                                            "王子",
                                            "國王",
                                            "伯爵夫人",
                                            "公主",
                                        ],
                                    },
                                },
                                {
                                    "description": "如果把公主打出在桌面，就會立刻出局。",
                                    "name": "公主",
                                    "value": 8,
                                    "usage": {
                                        "can_discard": True,
                                        "choose_players": [],
                                        "can_guess_cards": [],
                                    },
                                },
                            ],
                            "name": "player-a",
                            "out": False,
                        },
                        "winner": None,
                        "start_player": "player-a",
                    }
                ],
                "final_winner": None,
            },
            response,
        )

        # 玩家出牌
        request_body = {"chosen_player": "player-b", "guess_card": "神父"}
        response = self.t.post(
            f"/games/{game_id}/player/player-a/card/衛兵/play", json=request_body
        ).json()
        self.assertEqual(
            {
                "game_id": game_id,
                "events": [
                    {"type": "round_started", "winner": None},
                    {
                        "card": "衛兵",
                        "to": "player-b",
                        "took_effect": {"event": None, "took": True},
                        "turn_player": "player-a",
                        "type": "card_action",
                        "with_card": "神父",
                    },
                    {"type": "round_started", "winner": "player-a"},
                ],
                "players": [
                    {"id": None, "name": "player-a", "score": 1},
                    {"id": None, "name": "player-b", "score": 0},
                ],
                "rounds": [
                    {
                        "players": [
                            {
                                "seen_cards": [],
                                "cards": [
                                    {
                                        "description": "如果把公主打出在桌面，就會立刻出局。",
                                        "name": "公主",
                                        "value": 8,
                                        "usage": {
                                            "can_discard": False,
                                            "choose_players": [],
                                            "can_guess_cards": [],
                                        },
                                    }
                                ],
                                "name": "player-a",
                                "out": False,
                            },
                            {
                                "cards": [
                                    {
                                        "description": "打出神父後，可以看一名玩家的所有手牌。",
                                        "name": "神父",
                                        "value": 2,
                                        "usage": {
                                            "can_discard": False,
                                            "choose_players": [],
                                            "can_guess_cards": [],
                                        },
                                    }
                                ],
                                "name": "player-b",
                                "seen_cards": [],
                                "out": True,
                            },
                        ],
                        "turn_player": {
                            "seen_cards": [],
                            "cards": [
                                {
                                    "description": "如果把公主打出在桌面，就會立刻出局。",
                                    "name": "公主",
                                    "value": 8,
                                    "usage": {
                                        "can_discard": False,
                                        "choose_players": [],
                                        "can_guess_cards": [],
                                    },
                                }
                            ],
                            "name": "player-a",
                            "out": False,
                        },
                        "winner": "player-a",
                        "start_player": "player-a",
                    },
                    {
                        "players": [
                            {
                                "seen_cards": [],
                                "cards": [
                                    {
                                        "description": "猜測一名對手的手牌(不可猜衛兵)，猜測正確對方立刻出局。",
                                        "name": "衛兵",
                                        "value": 1,
                                        "usage": {
                                            "can_discard": True,
                                            "choose_players": ["player-b"],
                                            "can_guess_cards": [
                                                "神父",
                                                "男爵",
                                                "侍女",
                                                "王子",
                                                "國王",
                                                "伯爵夫人",
                                                "公主",
                                            ],
                                        },
                                    },
                                    {
                                        "description": "如果把公主打出在桌面，就會立刻出局。",
                                        "name": "公主",
                                        "value": 8,
                                        "usage": {
                                            "can_discard": True,
                                            "choose_players": [],
                                            "can_guess_cards": [],
                                        },
                                    },
                                ],
                                "name": "player-a",
                                "out": False,
                            },
                            {
                                "cards": [],
                                "seen_cards": [],
                                "name": "player-b",
                                "out": False,
                            },
                        ],
                        "turn_player": {
                            "seen_cards": [],
                            "cards": [
                                {
                                    "description": "猜測一名對手的手牌(不可猜衛兵)，猜測正確對方立刻出局。",
                                    "name": "衛兵",
                                    "value": 1,
                                    "usage": {
                                        "can_discard": True,
                                        "choose_players": ["player-b"],
                                        "can_guess_cards": [
                                            "神父",
                                            "男爵",
                                            "侍女",
                                            "王子",
                                            "國王",
                                            "伯爵夫人",
                                            "公主",
                                        ],
                                    },
                                },
                                {
                                    "description": "如果把公主打出在桌面，就會立刻出局。",
                                    "name": "公主",
                                    "value": 8,
                                    "usage": {
                                        "can_discard": True,
                                        "choose_players": [],
                                        "can_guess_cards": [],
                                    },
                                },
                            ],
                            "name": "player-a",
                            "out": False,
                        },
                        "winner": None,
                        "start_player": "player-a",
                    },
                ],
                "final_winner": None,
            },
            response,
        )
