from typing import Union

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from love_letter.repository import create_default_repository
from love_letter.service import GameService
from love_letter.web.dto import GameStatus, GuessCard, ToSomeoneCard

app = FastAPI()
service = GameService(create_default_repository())
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
    return service.create_game(player_id)


@app.post("/games/{game_id}/player/{player_id}/join")
async def join_game(game_id: str, player_id: str) -> bool:
    return service.join_game(game_id, player_id)


@app.post("/games/{game_id}/start")
async def start_game(game_id: str):
    return service.start_game(game_id)


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
    return service.play_card(game_id, player_id, card_name, card_action)


@app.get("/games/{game_id}/player/{player_id}/status", response_model=GameStatus)
async def get_status(game_id: str, player_id: str):
    return service.get_status(game_id, player_id)


if __name__ == "__main__":
    uvicorn.run("love_letter.web.app:app", host="0.0.0.0", port=8080, reload=True)
