from typing import List

from pydantic import BaseModel


class GuessCard(BaseModel):
    chosen_player: str
    guess_card: str


class ToSomeoneCard(BaseModel):
    chosen_player: str
