from typing import Union

import uvicorn
from fastapi import FastAPI

from love_letter.repository import GameRepositoryInMemoryImpl
from love_letter.service import GameService
from love_letter.web.dto import GuessCard, ToSomeoneCard

app = FastAPI()
service = GameService(GameRepositoryInMemoryImpl())


@app.post("/games/create/by_player/{player_id}")
async def create_game(player_id: str) -> str:
    return service.create_game(player_id)


@app.post("/games/{game_id}/player/{player_id}/join")
async def join_game(game_id: str, player_id: str) -> bool:
    return service.join_game(game_id, player_id)


@app.post("/games/{game_id}/start")
async def start_game(game_id: str):
    return service.start_game(game_id)


@app.post("/games/{game_id}/player/{player_id}/card/{card_name}/play")
async def play_card(
        game_id: str, player_id: str, card_name: str, card_action: Union[GuessCard, ToSomeoneCard, None] = None
):
    return service.play_card(game_id, player_id, card_name, card_action)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8080)
