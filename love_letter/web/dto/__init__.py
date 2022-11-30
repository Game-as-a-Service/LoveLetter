from typing import List

from pydantic import BaseModel


class GuessCard(BaseModel):
    opponent: str
    guess_card: str


class ToSomeoneCard(BaseModel):
    opponent: str
