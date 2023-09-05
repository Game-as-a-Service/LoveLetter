from typing import Any, Dict, List

from pydantic import BaseModel


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
    id: str | None


class GameStatus(BaseModel):
    game_id: str
    players: List[NamedPlayer]
    events: List[Dict]
    rounds: List[RoundModel]
    final_winner: str | None


class LobbyPlayer(BaseModel):
    id: str
    nickname: str


class LobbyPlayers(BaseModel):
    players: List[LobbyPlayer]
