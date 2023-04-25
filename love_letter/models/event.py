from dataclasses import dataclass


class DomainEvent:
    pass


@dataclass
class GameCreatedEvent(DomainEvent):
    game_id: str
