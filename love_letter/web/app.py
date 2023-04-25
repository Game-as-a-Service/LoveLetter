from typing import Union

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from love_letter.models import GuessCard, ToSomeoneCard
from love_letter.usecase.create_game import CreateGame
from love_letter.usecase.get_status import GetStatus
from love_letter.usecase.join_game import JoinGame
from love_letter.usecase.play_card import PlayCard
from love_letter.usecase.start_game import StartGame
from love_letter.web.dto import GameStatus
from love_letter.web.presenter import CreateGamePresenter, build_player_view

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
async def create_game(player_id: str) -> str:
    presenter = CreateGamePresenter.presenter()
    CreateGame().execute(CreateGame.input(player_id), presenter)
    return presenter.as_view_model()


@app.post("/games/{game_id}/player/{player_id}/join")
async def join_game(game_id: str, player_id: str) -> bool:
    presenter = JoinGame.presenter()
    JoinGame().execute(JoinGame.input(game_id, player_id), presenter)
    return presenter.as_view_model()


@app.post("/games/{game_id}/start")
async def start_game(game_id: str):
    presenter = StartGame.presenter()
    StartGame().execute(StartGame.input(game_id), presenter)
    return presenter.as_view_model()


@app.post(
    "/games/{game_id}/player/{player_id}/card/{card_name}/play",
    response_model=GameStatus,
)
async def play_card(
    game_id: str,
    player_id: str,
    card_name: str,
    card_action: Union[GuessCard, ToSomeoneCard, None] = None,
):
    presenter = PlayCard.presenter()
    PlayCard().execute(
        PlayCard.input(game_id, player_id, card_name, card_action), presenter
    )
    game = presenter.as_view_model()
    return build_player_view(game, player_id)


@app.get("/games/{game_id}/player/{player_id}/status", response_model=GameStatus)
async def get_status(game_id: str, player_id: str):
    presenter = GetStatus.presenter()
    GetStatus().execute(GetStatus.input(game_id, player_id), presenter)
    game = presenter.as_view_model()
    return build_player_view(game, player_id)


def run():
    uvicorn.run("love_letter.web.app:app", host="0.0.0.0", port=8080, reload=True)


if __name__ == "__main__":
    run()
