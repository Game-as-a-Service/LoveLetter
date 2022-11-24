from typing import List

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

from love_letter.service import GameService

app = FastAPI()
service = GameService()


@app.post("/games/{game_id}/start")
async def start_game(game_id: str):
    return service.start_game(game_id)


class CardAction(BaseModel):
    turn_player: str
    opponent: str
    card_action: List[int]


@app.post("/games/{game_id}/play")
async def play_card(game_id: str, card_action: CardAction):
    return service.play_card(game_id, card_action)
