import secrets
from copy import deepcopy
from dataclasses import dataclass
from typing import List, Union, Optional
from operator import attrgetter

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
            deck.draw_card(p)
        return deck

    def next_turn_player(self, last_winner: str = None) -> bool:
        """
        True if the round keeps going, otherwise false.

        For example:
        1. the deck is empty will cause the round ended
        1. only one player alive will cause the round ended
        """
        # TODO should fix the side effect (when empty deck, it should not be moved) before making player-context
        self._shift_to_next_player(last_winner)

        # Remove player protected after one round
        self.turn_player.protected = False
        return self.deck.draw_card(self.turn_player)

    def _shift_to_next_player(self, last_winner: str = None):
        # assign the turn player from the last winner
        if last_winner is not None:
            for player in self.players:
                if player.name == last_winner:
                    self.turn_player = player
                    return

        # pick up a player for the first round
        if self.turn_player is None:
            self.turn_player = Round.choose_one_randomly(self.players)
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

    def next_round(self, last_winner: str = None):
        # TODO if we arrive the ending of the game, show the lucky person who won the Princess
        round = Round(deepcopy(self.players))
        round.next_turn_player(last_winner)
        self.rounds.append(round)

    def to_dict(self):
        return dict(game_id=self.id, players=[x.to_dict() for x in self.players],
                    rounds=[x.to_dict() for x in self.rounds])

    def play(self, player_id: str, card_name: str, card_action: Union[GuessCard, ToSomeoneCard, None]):
        if self.find_player_by_id(player_id) != self.get_turn_player():
            raise ValueError(f"{player_id} is not a turn player")

        players = self.this_round_players()

        # TODO rewrite handles to chain of rules and catching lost cases
        turn_player: "Player" = self.find_player_by_id(player_id)
        discarded_card: "Card" = find_card_by_name(card_name)
        self.handle_when_guess_card_action(turn_player, discarded_card, card_action)
        self.handle_when_to_someone_action(turn_player, discarded_card, card_action)
        self.handle_when_to_nothing_action(turn_player, discarded_card, card_action)

        self.rounds[-1].draw_card_by_system(players)

        # 出牌後，有玩家可能出局，剩最後一名玩家，它就是勝利者
        self.find_winner(players)
    def handle_when_guess_card_action(self, turn_player: "Player", discarded_card: "Card", action: GuessCard):
        if not isinstance(action, GuessCard):
            return

        chosen_player: "Player" = self.find_player_by_id(action.chosen_player)

        turn_player.discard_card(chosen_player=chosen_player, discarded_card=discarded_card,
                                 with_card=find_card_by_name(action.guess_card))

    def find_player_by_id(self, player_id):
        players = self.this_round_players()
        for x in players:
            if x.name == player_id:
                return x
        raise ValueError(f"Cannot find the player with id: {player_id}")

    def this_round_players(self):
        return self.rounds[-1].players

    def handle_when_to_someone_action(self, turn_player: "Player", discarded_card: "Card", action: ToSomeoneCard):
        if not isinstance(action, ToSomeoneCard):
            return

        chosen_player: "Player" = self.find_player_by_id(action.chosen_player)
        turn_player.discard_card(chosen_player, discarded_card)

    def handle_when_to_nothing_action(self, turn_player: "Player", discarded_card: "Card", action: None):
        if action is not None:
            # Don't go there
            return

        turn_player.discard_card(turn_player, discarded_card)

    @classmethod
    def create(cls, player: "Player") -> "Game":
        game = Game()
        game.join(player)
        return game

    def has_started(self):
        return len(self.rounds) > 0

    def get_turn_player(self):
        return self.rounds[-1].turn_player

    def next_turn_player(self) -> bool:
        return self.rounds[-1].next_turn_player()

    def find_winner(self, players: List["Player"]):
        might_has_winner = [x for x in players if not x.am_i_out]
        if len(might_has_winner) == 1:
            winner_name = might_has_winner[0].name
            # increase token of affection in game player
            # 這幾個 for loop 都很像，是否要開一個 method
            for player in self.players:
                if player.name == winner_name:
                    player.tokens_of_affection += 1
            # increase token of affection in round player
            for player in players:
                if player.name == winner_name:
                    player.tokens_of_affection += 1
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
            might_has_winner = list(filter(lambda x: x.cards[0].value == biggest_card_value, might_has_winner))
            # 當手牌大小一樣時，比較棄牌堆的總和
            if len(might_has_winner) != 1:
                winner = max(might_has_winner, key=attrgetter('total_value_of_card'))
            for player in self.players:
                if player.name == winner.name:
                    player.tokens_of_affection += 1
            for player in players:
                if player.name == winner.name:
                    player.tokens_of_affection += 1
            self.rounds[-1].winner = winner.name
            self.next_round(winner.name)
            return


@dataclass
class Seen:
    opponent_name: str
    card: Card


class Player:

    def __init__(self):
        self.name: str = None
        self.cards: List[Card] = []
        self.am_i_out: bool = False
        self.protected = False
        self.total_value_of_card: int = 0
        self.seen_cards: List[Seen] = []
        self.tokens_of_affection: int = 0

    def discard_card(self, chosen_player: "Player" = None, discarded_card: Card = None, with_card: "Card" = None):
        # Precondition: the player must hold 2 cards
        if len(self.cards) != 2:
            return False

        # Precondition: Check will_be_played_card is in the hands
        if not any([True for c in self.cards if c.name == discarded_card.name]):
            raise GameException("Cannot discard cards not in your hand")

        if not (chosen_player and chosen_player.protected):
            discarded_card.trigger_effect(self, chosen_player=chosen_player, with_card=with_card)

        # TODO postcondition: the player holds 1 card after played
        self.drop_card(discarded_card)

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

    def __repr__(self):
        return f"Player({self.name},{self.cards})"

    def __gt__(self, other: "Player"):
        if len(self.cards) == 1 and len(other.cards) == 1:
            return self.cards[0].value > other.cards[0].value

    @classmethod
    def create(cls, name):
        p = Player()
        p.name = name
        return p

    def drop_card(self, discarded_card: Card):
        # only drop 1 card
        for index, card in enumerate(self.cards):
            if card.name == discarded_card.name:
                self.cards.pop(index)
                break
