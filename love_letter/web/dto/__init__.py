from typing import List

from pydantic import BaseModel


class CardAction(BaseModel):
    turn_player: str
    opponent: str
    card_action: List[str]
