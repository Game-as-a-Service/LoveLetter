from unittest.mock import patch

from fastapi.testclient import TestClient

from love_letter.config import config
from love_letter.models import Round
from love_letter.web.app import app
from love_letter.web.auth import JWTBearer
from love_letter.web.dto import GameStatus
from tests import LoveLetterRepositoryAwareTestCase
from tests.test_game_service import get_status


class LobbyTestCase(LoveLetterRepositoryAwareTestCase):
    def setUp(self) -> None:
        self.t: TestClient = TestClient(app)
        self.jwt_token: str = JWTBearer.create_jwt()
        self.game_id: str = self.__class__.game_id
        # disable random-picker for the first round
        # it always returns the first player
        self.origin_choose_one_randomly = Round.choose_one_randomly
        Round.choose_one_randomly = lambda players: players[0]

    @classmethod
    def setUpClass(cls):
        super(LobbyTestCase, cls).setUpClass()
        cls.game_id: str = ""

    def tearDown(self) -> None:
        Round.choose_one_randomly = self.origin_choose_one_randomly
        self.t.close()

    def test_health_api(self):
        response = self.t.get("/health")
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])

    def test_1_start_game(self):
        players = [
            {"id": "6497f6f226b40d440b9a90cc", "nickname": "板橋金城武"},
            {"id": "6498112b26b40d440b9a90ce", "nickname": "三重彭于晏"},
            {"id": "6499df157fed0c21a4fd0425", "nickname": "蘆洲劉德華"},
            {"id": "649836ed7fed0c21a4fd0423", "nickname": "永和周杰倫"},
        ]

        response = self.t.post(
            "/games",
            json=dict(players=players),
            headers={"Authorization": self.jwt_token},
        )
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertTrue(data["url"].startswith(config.FRONTEND_HOST))
        self.game_id = data["url"].split("/")[-1]
        self.__class__.game_id = self.game_id
        status_of_player: GameStatus = GameStatus.parse_obj(
            get_status(self.game_id, players[0]["nickname"])
        )

        status_players = status_of_player.players
        self.assertEqual(status_of_player.game_id, self.game_id)
        self.assertEqual(
            [p.name for p in status_players], [p["nickname"] for p in players]
        )
        self.assertEqual([p.id for p in status_players], [p["id"] for p in players])

    @patch("love_letter.web.app.JWTBearer")
    def test_2_game_status(self, mock_jwt_bearer):
        # 把呼叫大平台 /users/me 的api給mock掉，因為我們自己創建的jwt token無法取得對應的player_id
        mock_jwt_bearer.get_player_id.return_value = "6497f6f226b40d440b9a90cc"
        response = self.t.get(
            f"/games/{self.game_id}/status", headers={"Authorization": self.jwt_token}
        )
        data = response.json()

        # 檢查是否mock了mock_jwt_bearer.get_player_id方法
        mock_jwt_bearer.get_player_id.assert_called_once_with(self.jwt_token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["game_id"], self.game_id)
        self.assertEqual(
            {
                "game_id": self.game_id,
                "events": [{"type": "round_started", "winner": None}],
                "players": [
                    {"id": "6497f6f226b40d440b9a90cc", "name": "板橋金城武", "score": 0},
                    {"id": "6498112b26b40d440b9a90ce", "name": "三重彭于晏", "score": 0},
                    {"id": "6499df157fed0c21a4fd0425", "name": "蘆洲劉德華", "score": 0},
                    {"id": "649836ed7fed0c21a4fd0423", "name": "永和周杰倫", "score": 0},
                ],
                "rounds": [
                    {
                        "players": [
                            {
                                "seen_cards": [],
                                "cards": [],
                                "name": "板橋金城武",
                                "out": False,
                            },
                            {
                                "cards": [],
                                "seen_cards": [],
                                "name": "三重彭于晏",
                                "out": False,
                            },
                            {
                                "cards": [],
                                "seen_cards": [],
                                "name": "蘆洲劉德華",
                                "out": False,
                            },
                            {
                                "cards": [],
                                "seen_cards": [],
                                "name": "永和周杰倫",
                                "out": False,
                            },
                        ],
                        "turn_player": {
                            "seen_cards": [],
                            "cards": [],
                            "name": "板橋金城武",
                            "out": False,
                        },
                        "winner": None,
                        "start_player": "板橋金城武",
                    }
                ],
                "final_winner": None,
            },
            data,
        )
