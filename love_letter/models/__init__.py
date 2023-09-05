import secrets
import uuid
from copy import deepcopy
from dataclasses import dataclass
from operator import attrgetter
from typing import Dict, List, Optional, Union

from pydantic import BaseModel

from love_letter.models.cards import Card, Deck, PriestCard, find_card_by_name

# isort: off
from love_letter.models.event import (
    DomainEvent,
    ExceptionEvent,
    PlayerJoinedEvent,
    StartGameEvent,
    CardPlayedEvent,
)

# isort: on
from love_letter.models.exceptions import GameException

num_of_player_with_tokens_to_win = {2: 7, 3: 5, 4: 4}


def deck_factory() -> Deck:
    return Deck()


class GuessCard(BaseModel):
    chosen_player: str
    guess_card: str


class ToSomeoneCard(BaseModel):
    chosen_player: str


class Round:
    winner: Optional[str] = None
    turn_player: Optional["Player"] = None
    start_player: str

    def __init__(self, players: List["Player"], deck: Optional[Deck] = None):
        self.players: List["Player"] = players

        if deck:
            self.deck = deck
        else:
            self.deck = self._setup_round(self.players)

    def _setup_round(self, players: List["Player"]):
        # make the deck replaceable for testing
        deck = deck_factory()
        deck.shuffle(len(players))

        # give each player a card
        for p in players:
            deck.draw_card(p)
        return deck

    def next_turn_player(self, last_winner: Optional[str] = None) -> bool:
        """
        True if the round keeps going, otherwise false.

        For example:
        1. the deck is empty will cause the round ended
        1. only one player alive will cause the round ended
        """
        # TODO should fix the side effect (when empty deck, it should not be moved) before making player-context
        self._shift_to_next_player(last_winner)

        if self.turn_player is None:
            raise ValueError("Turn player is not assigned yet.")
        # Remove player protected after one round
        self.turn_player.protected = False
        return self.deck.draw_card(self.turn_player)

    def _shift_to_next_player(self, last_winner: Optional[str]):
        # assign the turn player from the last winner
        if last_winner is not None:
            for player in self.players:
                if player.name == last_winner:
                    self.turn_player = player
                    self.start_player = self.turn_player.name
                    return

        # pick up a player for the first round
        if self.turn_player is None:
            self.turn_player = Round.choose_one_randomly(self.players)
            self.start_player = self.turn_player.name
            return

        from_index = self.players.index(self.turn_player)

        for _ in range(1, len(self.players)):
            from_index = from_index + 1
            if from_index >= len(self.players):
                selected = self.players[from_index - len(self.players)]
            else:
                selected = self.players[from_index]

            if not selected.am_i_out:
                self.turn_player = selected
                break

    @classmethod
    def choose_one_randomly(cls, players: List["Player"]):
        return players[secrets.randbelow(len(players))]

    def draw_card_by_system(self, players: List["Player"]):
        """
        Make sure each players has one card and
        help the player with one less card to draw a card.
        If deck card is empty, will draw remove_by_rule_card
        :param players:
        :return:
        """
        player = None

        for p in players:
            if not p.am_i_out and len(p.cards) != 1:
                player = p
                continue

        # if don't get player or player has card return
        if not player or len(player.cards):
            return

        if not self.deck.draw_card(player):
            self.deck.draw_remove_card(player)


class Game:
    def __init__(self):
        self.id: Optional[str] = uuid.uuid4().hex
        self.players: List["Player"] = []
        self.rounds: List["Round"] = []
        self.num_of_tokens_to_win: int = 0
        self.final_winner: Optional[str] = None
        self.events: List[Dict] = []

    def post_event(self, message: Dict):
        self.events.append(message)

    def join(self, player: "Player") -> List[PlayerJoinedEvent]:
        if self.has_started():
            raise GameException(ExceptionEvent(message="Game Has Started"))
        # TODO it is no way to verify two players with same name, just pass it
        join_before = [p for p in self.players if p.name == player.name]
        if join_before:
            return []

        if len(self.players) < 4:
            self.players.append(player)
            return [PlayerJoinedEvent(game_id=self.id, success=True)]

        raise GameException(
            ExceptionEvent(message="Game Has No Capacity For New Players")
        )

    def start(self) -> List[DomainEvent]:
        if len(self.players) < 2:
            raise GameException("Too Few Players")
        self.num_of_tokens_to_win = num_of_player_with_tokens_to_win.get(
            len(self.players)
        )
        self.next_round()
        return [StartGameEvent(success=True)]

    def next_round(self, last_winner: Optional[str] = None):
        # TODO if we arrive the ending of the game, show the lucky person who won the Princess
        if last_winner is not None:
            players = self.rounds[-1].players
            for player in self.players:
                if player.name == last_winner:
                    player.tokens_of_affection += 1
            for player in players:
                if player.name == last_winner:
                    player.tokens_of_affection += 1
        for player in self.players:
            if player.tokens_of_affection == self.num_of_tokens_to_win:
                self.final_winner = player.name
                self.post_event(
                    {"type": "game_over", "final_winner": self.final_winner}
                )
                return
        round = Round(deepcopy(self.players))
        round.next_turn_player(last_winner)
        self.post_event({"type": "round_started", "winner": last_winner})
        self.rounds.append(round)

    def play(
        self,
        player_id: str,
        card_name: str,
        card_action: Union[GuessCard, ToSomeoneCard, None],
    ):
        if self.find_player_by_id(player_id) != self.get_turn_player():
            raise ValueError(f"{player_id} is not a turn player")

        players = self.this_round_players()

        turn_player: "Player" = self.find_player_by_id(player_id)
        discarded_card: "Card" = find_card_by_name(card_name)
        self.handle_card_action(turn_player, discarded_card, card_action)

        self.rounds[-1].draw_card_by_system(players)

        # 出牌後，有玩家可能出局，剩最後一名玩家，它就是勝利者
        self.find_winner(players)
        return [CardPlayedEvent(self)]

    def find_player_by_id(self, player_id):
        players = self.this_round_players()
        for x in players:
            if x.name == player_id:
                return x
        raise ValueError(f"Cannot find the player with id: {player_id}")

    def this_round_players(self):
        return self.rounds[-1].players

    @classmethod
    def create(cls, player: "Player") -> "Game":
        game = Game()
        game.join(player)
        return game

    def has_started(self):
        return len(self.rounds) > 0

    def get_turn_player(self, round_index: int = -1):
        """Return the turn player of the given round."""
        turn_player = self.rounds[round_index].turn_player
        if turn_player is None:
            raise ValueError("Turn player is not assigned.")
        return turn_player

    def next_turn_player(self) -> bool:
        return self.rounds[-1].next_turn_player()

    def find_winner(self, players: List["Player"]):
        might_has_winner = [x for x in players if not x.am_i_out]
        if len(might_has_winner) == 1:
            winner_name = might_has_winner[0].name
            self.rounds[-1].winner = winner_name
            self.next_round(winner_name)
            return
        has_next_player = self.next_turn_player()
        if not has_next_player:
            # TODO it doesn't cover the case: two players own same card but different total values (score)
            # find the winner from the alive players
            # 牌庫抽完，比較手牌大小
            winner = might_has_winner[0]
            for x in might_has_winner:
                # get the biggest card value from alive players
                if x.cards[0].value > winner.cards[0].value:
                    winner = x
            biggest_card_value = winner.cards[0].value
            # collect all the players that has the biggest card value
            might_has_winner = list(
                filter(
                    lambda x: x.cards[0].value == biggest_card_value, might_has_winner
                )
            )
            # 當手牌大小一樣時，比較棄牌堆的總和
            if len(might_has_winner) != 1:
                winner = max(might_has_winner, key=attrgetter("total_value_of_card"))
            self.rounds[-1].winner = winner.name
            self.next_round(winner.name)
            return

    def handle_card_action(
        self,
        turn_player: "Player",
        discarded_card: "Card",
        action: Union[GuessCard, ToSomeoneCard, None],
    ) -> None:
        """
        Handles all card actions like GuessCard, ToSomeoneCard and None
        :param turn_player:
        :param discarded_card:
        :param action:
        :return:
        """
        if action is None:
            took_effect = turn_player.discard_card(turn_player, discarded_card)
            self.post_event(
                dict(
                    type="card_action",
                    turn_player=turn_player.name,
                    card=discarded_card.name,
                    took_effect=took_effect,
                )
            )
            return

        with_card = None
        if isinstance(action, GuessCard):
            with_card = find_card_by_name(action.guess_card)

        chosen_player: "Player" = self.find_player_by_id(action.chosen_player)
        took_effect = turn_player.discard_card(chosen_player, discarded_card, with_card)
        if with_card:
            self.post_event(
                dict(
                    type="card_action",
                    turn_player=turn_player.name,
                    card=discarded_card.name,
                    to=chosen_player.name,
                    with_card=with_card.name,
                    took_effect=took_effect,
                )
            )
        else:
            self.post_event(
                dict(
                    type="card_action",
                    turn_player=turn_player.name,
                    card=discarded_card.name,
                    to=chosen_player.name,
                    took_effect=took_effect,
                )
            )


@dataclass
class Seen:
    opponent_name: str
    card: Card


class Player:
    def __init__(self, name: str, _id: Union[str] = None):
        self.id = _id
        self.name = name
        self.cards: List[Card] = []
        self.am_i_out: bool = False
        self.protected: bool = False
        self.total_value_of_card: int = 0
        self.seen_cards: List[Seen] = []
        self.tokens_of_affection: int = 0

    def discard_card(
        self,
        chosen_player: "Player",
        discarded_card: "Card",
        with_card: Optional["Card"] = None,
    ):
        # Precondition: the player must hold 2 cards
        if len(self.cards) != 2:
            return dict(took=False, event=None)

        # Precondition: Check will_be_played_card is in the hands
        if not any([True for c in self.cards if c.name == discarded_card.name]):
            raise GameException("Cannot discard cards not in your hand")

        self.drop_card(discarded_card)
        trigger_event = None
        if not (chosen_player and chosen_player.protected):
            trigger_event = discarded_card.trigger_effect(
                self, chosen_player=chosen_player, with_card=with_card
            )
        elif (chosen_player and chosen_player.protected) and trigger_event is None:
            trigger_event = dict(
                trigger_by=discarded_card.name, protected=chosen_player.name
            )

        if len(self.cards) != 1:
            return dict(took=False, event=trigger_event)

        self.total_value_of_card += discarded_card.value
        return dict(took=True, event=trigger_event)

    def out(self):
        self.am_i_out = True

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return f"Player({self.name},{self.cards})"

    def __lt__(self, other: "Player"):
        if len(self.cards) == 1 and len(other.cards) == 1:
            return self.cards[0].value < other.cards[0].value

    def __gt__(self, other: "Player"):
        if len(self.cards) != 1 or len(other.cards) != 1:
            raise AssertionError("Unable to compare players.")
        elif self.cards[0].value == other.cards[0].value:
            return self.total_value_of_card > other.total_value_of_card
        else:
            return self.cards[0].value > other.cards[0].value

    def drop_card(self, discarded_card: Card):
        # only drop 1 card
        for index, card in enumerate(self.cards):
            if card.name == discarded_card.name:
                self.cards.pop(index)
                break
