from typing import List

from pydantic import BaseModel


class GuessCard(BaseModel):
    chosen_player: str
    guess_card: str


class ToSomeoneCard(BaseModel):
    chosen_player: str


class CardModel(BaseModel):
    name: str
    description: str
    value: int
    can_discard: bool
    choose_players: List[str]
    can_guess_cards: List[str]


class PlayerModel(BaseModel):
    name: str | None
    out: bool
    cards: List[CardModel]


class RoundModel(BaseModel):
    players: List[PlayerModel]
    winner: str | None
    turn_player: PlayerModel


class GameStatus(BaseModel):
    game_id: str
    rounds: List[RoundModel]
