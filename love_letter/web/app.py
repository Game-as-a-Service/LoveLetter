from typing import Union

import uvicorn
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from love_letter.models import GuessCard, ToSomeoneCard
from love_letter.usecase.create_game import CreateGame
from love_letter.usecase.get_status import GetStatus
from love_letter.usecase.join_game import JoinGame
from love_letter.usecase.lobby_start_game import LobbyStartGame
from love_letter.usecase.play_card import PlayCard
from love_letter.usecase.start_game import StartGame
from love_letter.web.auth import JWTBearer
from love_letter.web.dto import GameStatus, LobbyPlayers

# isort: off
from love_letter.web.presenter import (
    CreateGamePresenter,
    JoinGamePresenter,
    StartGamePresenter,
    build_player_view,
    PlayCardPresenter,
    GetStatusPresenter,
    LobbyStartGamePresenter,
)

# isort: on

app = FastAPI()
origins = ["*", "http://localhost:3000", "http://localhost:8080"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "HEAD", "POST", "OPTIONS"],
    allow_headers=[
        "accept",
        "content-type",
        "content-language",
        "accept-language",
        "Access-Control-Allow-Origin",
        "Access-Control-Allow-Credentials",
    ],
)


@app.post("/games/create/by_player/{player_id}")
def create_game(player_id: str) -> str:
    presenter = CreateGamePresenter.presenter()
    CreateGame().execute(CreateGame.input(player_id), presenter)
    return presenter.as_view_model()


@app.post("/games/{game_id}/player/{player_id}/join")
def join_game(game_id: str, player_id: str) -> bool:
    presenter = JoinGamePresenter.presenter()
    JoinGame().execute(JoinGame.input(game_id, player_id), presenter)
    return presenter.as_view_model()


@app.post("/games/{game_id}/start")
def start_game(game_id: str):
    presenter = StartGamePresenter.presenter()
    StartGame().execute(StartGame.input(game_id), presenter)
    return presenter.as_view_model()


@app.post(
    "/games/{game_id}/player/{player_id}/card/{card_name}/play",
    response_model=GameStatus,
)
def play_card(
    game_id: str,
    player_id: str,
    card_name: str,
    card_action: Union[GuessCard, ToSomeoneCard, None] = None,
):
    presenter = PlayCardPresenter.presenter()
    PlayCard().execute(
        PlayCard.input(game_id, player_id, card_name, card_action), presenter
    )
    game = presenter.as_view_model()
    return build_player_view(game, player_id)


@app.get("/games/{game_id}/player/{player_id}/status", response_model=GameStatus)
def get_status(game_id: str, player_id: str):
    presenter = GetStatusPresenter.presenter()
    GetStatus().execute(GetStatus.input(game_id, player_id), presenter)
    game = presenter.as_view_model()
    return build_player_view(game, player_id)


@app.post("/games", dependencies=[Depends(JWTBearer())])
def lobby_start_game(players: LobbyPlayers):
    presenter = LobbyStartGamePresenter.presenter()
    LobbyStartGame().execute(players, presenter)
    return presenter.as_view_model()


@app.get("/heath")
def heath():
    return {"success": True}


def run():
    uvicorn.run("love_letter.web.app:app", host="0.0.0.0", port=8080, reload=True)


if __name__ == "__main__":
    run()
