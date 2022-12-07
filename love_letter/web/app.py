from typing import Union

from fastapi import FastAPI

from love_letter.service import GameService
from love_letter.web.dto import GuessCard, ToSomeoneCard

app = FastAPI()
service = GameService()


@app.post("/games/{game_id}/start")
async def start_game(game_id: str):
    return service.start_game(game_id)


@app.post("/games/{game_id}/player/{player_id}/card/{card_name}/play")
async def play_card(
        game_id: str, player_id: str, card_name: str, card_action: Union[GuessCard, ToSomeoneCard, None] = None
):
    return service.play_card(game_id, player_id, card_name, card_action)
