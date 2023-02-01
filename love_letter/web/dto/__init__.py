from typing import Any, Dict, List

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
    usage: Dict[str, Any]


class SeenData(BaseModel):
    opponent_name: str
    card: CardModel


class PlayerModel(BaseModel):
    name: str | None
    out: bool
    cards: List[CardModel]
    seen_cards: List[SeenData]


class RoundModel(BaseModel):
    players: List[PlayerModel]
    winner: str | None
    turn_player: PlayerModel
    start_player: str


class NamedPlayer(BaseModel):
    name: str | None
    score: int


class GameStatus(BaseModel):
    game_id: str
    players: List[NamedPlayer]
    events: List[Dict]
    rounds: List[RoundModel]
