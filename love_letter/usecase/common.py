import abc
from typing import List

from love_letter.models.event import DomainEvent
from love_letter.repository import create_default_repository

game_repository = create_default_repository()


class Presenter(metaclass=abc.ABCMeta):
    def __init__(self):
        self.events: List[DomainEvent] = []

    def present(self, events: List[DomainEvent]):
        self.events = events

    @abc.abstractmethod
    def as_view_model(self):
        pass
