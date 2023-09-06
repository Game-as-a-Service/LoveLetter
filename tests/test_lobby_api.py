from starlette.testclient import TestClient

from love_letter.config import FRONTEND_HOST
from love_letter.web.app import app
from love_letter.web.dto import GameStatus
from tests import LoveLetterRepositoryAwareTestCase
from tests.test_game_service import get_status


class LobbyTestCase(LoveLetterRepositoryAwareTestCase):
    def setUp(self) -> None:
        self.t: TestClient = TestClient(app)
        # fixme: token會過期，導致之後jwt token驗證失敗，後續測試無效
        self.scheme: str = "Bearer"
        self.token: str = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImlrN3l5VkpoM3pFSW1hLWduZ2lTRCJ9.eyJpc3MiOiJodHRwczovL2Rldi0xbDBpeGp3OHlvaHNsdW9pLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDEwNjQ4ODA3MDcyNjU5MDQ1NDEyMyIsImF1ZCI6WyJodHRwczovL2FwaS5nYWFzLndhdGVyYmFsbHNhLnR3IiwiaHR0cHM6Ly9kZXYtMWwwaXhqdzh5b2hzbHVvaS51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjk0MDA4MzI3LCJleHAiOjE2OTQwMTE5MjcsImF6cCI6IjBaN2huRGxkNXRyUHFpMnYwbGxvQlk3NE1IZERZR0V5Iiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCBvZmZsaW5lX2FjY2VzcyJ9.iH5rk7NnhstQvoG8rs0uWLcnxZrylQDUWMA_qK7S0CVfnX91P6EivQqdz6vscCjnRDuki2XpprIs3Fhs-xLtE3a44L02JNcu-wkeDPWChsY238cW_lh3SMXX_ssxmZwWWwcIBJOLy3DgKg02Aj-u9LzdEjZZNB-XwLEltme-UtZlRuNtR8dldiPs4wruEqjQ-Qy4ka7mQi6qzwjzQonO1efDfWqgN7W0Rqn2id06qgVgxI0wYdB3qUWL2kuRxiYB4NYqheAo1IfKmyvceNBc5y6UroDfc324jIT7O8yaJmj6aMmnUJEY8e5f7L4AnHyKzJeBUMdjhy80VihdxgnOTw"
        self.jwt_token: str = f"{self.scheme} {self.token}"

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
        ).json()
        self.assertTrue(response["url"].startswith(FRONTEND_HOST))
        game_id = response["url"].split("/")[-1]
        status_of_player: GameStatus = GameStatus.parse_obj(
            get_status(game_id, players[0]["nickname"])
        )

        status_players = status_of_player.players
        self.assertEqual(status_of_player.game_id, game_id)
        self.assertEqual(
            [p.name for p in status_players], [p["nickname"] for p in players]
        )
        self.assertEqual([p.id for p in status_players], [p["id"] for p in players])
