from dataclasses import dataclass


class DomainEvent:
    pass


@dataclass
class GameCreatedEvent(DomainEvent):
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
