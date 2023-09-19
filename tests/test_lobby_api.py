from starlette.testclient import TestClient

from love_letter.config import config
from love_letter.web.app import app
from love_letter.web.auth import JWTBearer
from love_letter.web.dto import GameStatus
from tests import LoveLetterRepositoryAwareTestCase
from tests.test_game_service import get_status


class LobbyTestCase(LoveLetterRepositoryAwareTestCase):
    def setUp(self) -> None:
        self.t: TestClient = TestClient(app)
        self.jwt_token: str = JWTBearer.create_jwt()

    def tearDown(self) -> None:
        self.t.close()

    def test_heath_api(self):
        response = self.t.get("/heath")
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])

    def test_start_game(self):
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
        game_id = data["url"].split("/")[-1]
        status_of_player: GameStatus = GameStatus.parse_obj(
            get_status(game_id, players[0]["nickname"])
        )

        status_players = status_of_player.players
        self.assertEqual(status_of_player.game_id, game_id)
        self.assertEqual(
            [p.name for p in status_players], [p["nickname"] for p in players]
        )
        self.assertEqual([p.id for p in status_players], [p["id"] for p in players])
