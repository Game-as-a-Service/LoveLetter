from copy import deepcopy
from copy import deepcopy
from dataclasses import dataclass
from typing import List, Union

from love_letter.models.cards import Card, Deck, PriestCard, find_card_by_name
from love_letter.models.exceptions import GameException
from love_letter.web.dto import GuessCard, ToSomeoneCard


def deck_factory() -> Deck:
    return Deck()


class Round:

    def __init__(self, players: List["Player"]):
        self.players: List["Player"] = players
        self.deck = self._setup_round(self.players)
        self.winner = None

        # turn player is set by game
        self.turn_player: Player = None

    def _setup_round(self, players: List["Player"]):
        # make the deck replaceable for testing
        deck = deck_factory()
        deck.shuffle(len(players))

        # give each player a card
        for p in players:
            deck.draw(p)
        return deck

    def next_turn_player(self):
        self._shift_to_next_player()
        self.deck.draw(self.turn_player)
        # TODO tell the game from return-value if the round has ended

    def _shift_to_next_player(self):
        # TODO only shift to players who is not out
        if self.turn_player is None:
            # TODO pick a turn player randomly if no one is turn player *FOR NOW*
            # TODO fix it by rules 1. first round => randomly, 2. non-first round, pick last winner as the turn player
            self.turn_player = self.players[0]
            return

        from_index = self.players.index(self.turn_player)
        for next_index in range(from_index + 1, len(self.players)):
            next_index = next_index % len(self.players)
            if not self.players[next_index].am_i_out:
                self.turn_player = self.players[next_index]
                return

    def to_dict(self):
        return dict(players=[x.to_dict() for x in self.players], winner=self.winner)


class Game:

    def __init__(self):
        self.id: str = None
        self.players: List["Player"] = []
        self.rounds: List["Round"] = []

    def join(self, player: "Player"):
        if self.has_started():
            raise GameException("Game Has Started")

        if len(self.players) < 4:
            self.players.append(player)
            return

        raise GameException("Game Has No Capacity For New Players")

    def start(self):
        if len(self.players) < 2:
            raise GameException("Too Few Players")

        self.next_round()

    def next_round(self):
        # TODO 如果沒有下一局，丟 exception
        round = Round(deepcopy(self.players))
        round.next_turn_player()
        self.rounds.append(round)

    def to_dict(self):
        return dict(game_id=self.id, players=[x.to_dict() for x in self.players],
                    rounds=[x.to_dict() for x in self.rounds])

    def play(self, player_id: str, card_name: str, card_action: Union[GuessCard, ToSomeoneCard, None]):
        if self.find_player_by_id(player_id) != self.get_turn_player():
            raise ValueError(f"{player_id} is not a turn player")

        players = self.this_round_players()

        # TODO rewrite handles to chain of rules and catching lost cases
        self.handle_when_guess_card_action(player_id, card_name, card_action)
        self.handle_when_to_someone_action(player_id, card_name, card_action)
        self.handle_when_to_nothing_action(player_id, card_name, card_action)

        # 出牌後，有玩家可能出局，剩最後一名玩家，它就是勝利者
        might_has_winner = [x for x in players if not x.am_i_out]
        if len(might_has_winner) == 1:
            self.rounds[-1].winner = might_has_winner[0].name
            self.next_round()
        self.next_turn_player()

    def handle_when_guess_card_action(self, player_id: str, card_name: str, action: GuessCard):
        if not isinstance(action, GuessCard):
            return

        turn_player: "Player" = self.find_player_by_id(player_id)
        chosen_player: "Player" = self.find_player_by_id(action.chosen_player)

        turn_player.discard_card(chosen_player=chosen_player, discarded_card=find_card_by_name(card_name),
                                 with_card=find_card_by_name(action.guess_card))

    def find_player_by_id(self, player_id):
        players = self.this_round_players()
        for x in players:
            if x.name == player_id:
                return x
        raise ValueError(f"Cannot find the player with id: {player_id}")

    def this_round_players(self):
        return self.rounds[-1].players

    def handle_when_to_someone_action(self, player_id: str, card_name: str, action: ToSomeoneCard):
        if not isinstance(action, ToSomeoneCard):
            return
        raise NotImplemented

    def handle_when_to_nothing_action(self, player_id: str, card_name: str, action):
        if action is not None:
            return

        raise NotImplemented

    @classmethod
    def create(cls, player: "Player") -> "Game":
        game = Game()
        game.join(player)
        return game

    def has_started(self):
        return len(self.rounds) > 0

    def get_turn_player(self):
        return self.rounds[-1].turn_player

    def next_turn_player(self):
        self.rounds[-1].next_turn_player()


@dataclass
class Seen:
    opponent_name: str
    card: Card


class Player:

    def __init__(self):
        self.name: str = None
        self.cards: List["Card"] = []
        self.am_i_out: bool = False
        self.protected = False
        self.total_value_of_card: int = 0
        self.seen_cards: List[Seen] = []

    def discard_card(self, chosen_player: "Player" = None, discarded_card: Card = None, with_card: "Card" = None):
        # TODO precondition: the player must hold 2 cards
        if len(self.cards) != 2:
            return False

        # Check will_be_played_card is in the hands
        if not any([True for c in self.cards if c.name == discarded_card.name]):
            return False

        if chosen_player and chosen_player.protected:
            # TODO send completed event for player
            return

        discarded_card.trigger_effect(self, chosen_player=chosen_player, with_card=with_card)

        # TODO postcondition: the player holds 1 card after played
        self.cards = list(filter(lambda x: x.name != discarded_card.name, self.cards))

        if len(self.cards) != 1:
            return False
        self.total_value_of_card += discarded_card.value

        return True

    def out(self):
        self.am_i_out = True

    def to_dict(self):
        return dict(name=self.name, out=self.am_i_out)

    def __eq__(self, other):
        return self.name == other.name

    @classmethod
    def create(cls, name):
        p = Player()
        p.name = name
        return p
