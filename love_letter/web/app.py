from fastapi import FastAPI

from love_letter.service import GameService
from love_letter.web.dto import CardAction

app = FastAPI()
service = GameService()


@app.post("/games/{game_id}/start")
async def start_game(game_id: str):
    return service.start_game(game_id)


@app.post("/games/{game_id}/play")
async def play_card(game_id: str, card_action: CardAction):
    return service.play_card(game_id, card_action)
