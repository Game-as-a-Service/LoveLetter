from fastapi.testclient import TestClient

from .main import app
# from love_letter.main import app

client = TestClient(app)


def test_read_main():
    print("test read main")
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_player_enter_game():
    response = client.post(
        "/enter_game",
        json={"player_name": "玩家A"}
    )
    print(response.status_code)
    print(response.json())


# if __name__ == '__main__':
#     test_player_enter_game()
