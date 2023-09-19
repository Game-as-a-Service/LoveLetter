from typing import Any, Dict, List, Optional

from love_letter.models import Game, PlayerJoinedEvent

# isort: off
from love_letter.models.event import (
    CardPlayedEvent,
    GetStatusEvent,
    StartGameEvent,
    GameEvent,
)

# isort: on
from love_letter.repository.data import GameData
from love_letter.usecase.common import Presenter


def build_player_view(game: Game, player_id: str):
    # we should remove private data for each player
    # players only know their own cards
    raw_result = GameData.to_dict(game)
    if len(raw_result["rounds"]) < 1:
        return raw_result

    last_round = raw_result["rounds"][-1]
    turn_player = last_round["turn_player"]

    for p in last_round["players"]:
        if p["name"] != player_id:
            p["cards"] = []
            p["seen_cards"] = []

    if turn_player["name"] != player_id:
        turn_player["cards"] = []
        turn_player["seen_cards"] = []

    return _decorate_with_card_usage(raw_result, player_id)


def _decorate_with_card_usage(raw_result, player_id):
    # Set previous round players cards can_discard=False、choose_players=[]
    if len(raw_result["rounds"]) > 1:
        for round in raw_result["rounds"][:-1]:
            for p in round["players"]:
                _add_cards_usage(p, None, True)
            _add_cards_usage(round["turn_player"], None, True)

    last_round = raw_result["rounds"][-1]
    turn_player = last_round["turn_player"]

    for p in last_round["players"]:
        if p["name"] == player_id:
            _add_cards_usage(p, turn_player)

    if turn_player["name"] == player_id:
        _add_cards_usage(turn_player, turn_player)

    return raw_result


def _add_cards_usage(
    player: Dict[str, Any],
    turn_player: Optional[Dict[str, Any]],
    previous_round: bool = False,
):
    """
    Add turn_player cards usage.
    :param player:
    :param turn_player:
    :param previous_round:
    :return:
    """
    for c in player["cards"]:
        # if is previous_round = True set 'can_discard'、'choose_players' to default value
        if previous_round:
            c["usage"]["can_discard"] = False
            c["usage"]["choose_players"] = []
            continue

        # if the player is not turn_player all cards can't be discarded
        if turn_player is None or player["name"] != turn_player["name"]:
            c["usage"]["can_discard"] = False

        # If this player can't discard and can't choose players
        if not c["usage"]["can_discard"]:
            c["usage"]["choose_players"] = []


class CreateGamePresenter(Presenter):
    def as_view_model(self):
        for event in self.events:
            if isinstance(event, PlayerJoinedEvent):
                return event.game_id
        raise BaseException("Game is unavailable.")

    @classmethod
    def presenter(cls) -> "CreateGamePresenter":
        return CreateGamePresenter()


class JoinGamePresenter(Presenter):
    def as_view_model(self):
        for event in self.events:
            if isinstance(event, PlayerJoinedEvent):
                return event.success
            elif isinstance(event, str):
                return event
        raise BaseException("Game is unavailable.")

    @classmethod
    def presenter(cls) -> "JoinGamePresenter":
        return JoinGamePresenter()


class StartGamePresenter(Presenter):
    def as_view_model(self):
        for event in self.events:
            if isinstance(event, StartGameEvent):
                return event.success
        raise BaseException("Game is unavailable.")

    @classmethod
    def presenter(cls) -> "StartGamePresenter":
        return StartGamePresenter()


class PlayCardPresenter(Presenter):
    def as_view_model(self) -> Game:
        for event in self.events:
            if isinstance(event, CardPlayedEvent):
                return event.game
        raise BaseException("Game is unavailable.")

    @classmethod
    def presenter(cls) -> "PlayCardPresenter":
        return PlayCardPresenter()


class GetStatusPresenter(Presenter):
    def as_view_model(self) -> Game:
        for event in self.events:
            if isinstance(event, GetStatusEvent):
                return event.game
        raise BaseException("Game is unavailable.")

    @classmethod
    def presenter(cls) -> "GetStatusPresenter":
        return GetStatusPresenter()


class LobbyStartGamePresenter(Presenter):
    def as_view_model(self):
        for event in self.events:
            if isinstance(event, GameEvent):
                return event
        raise BaseException("Game is unavailable.")

    @classmethod
    def presenter(cls) -> "LobbyStartGamePresenter":
        return LobbyStartGamePresenter()
