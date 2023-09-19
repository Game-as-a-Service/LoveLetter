from dataclasses import dataclass


class DomainEvent:
    pass


@dataclass
class PlayerJoinedEvent(DomainEvent):
    game_id: str
    success: bool


@dataclass
class ExceptionEvent(DomainEvent):
    message: str

    def __str__(self):
        return self.message


@dataclass
class StartGameEvent(DomainEvent):
    success: bool


@dataclass
class CardPlayedEvent(DomainEvent):
    game: "Game"


@dataclass
class GetStatusEvent(DomainEvent):
    game: "Game"


@dataclass
class GameEvent(DomainEvent):
    url: str
