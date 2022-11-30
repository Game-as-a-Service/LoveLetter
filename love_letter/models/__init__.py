from copy import deepcopy
from typing import List, Union

from love_letter.models.cards import find_card_by_name
from love_letter.web.dto import GuessCard, ToSomeoneCard


class Round:

    def __init__(self, players: List["Player"]):
        self.players: List["Player"] = players
        self.winner = None

    def to_dict(self):
        return dict(players=[x.to_dict() for x in self.players], winner=self.winner)


class Game:

    def __init__(self):
        self.id: str = None
        self.players: List["Player"] = []
        self.rounds: List["Round"] = []

    def add_player(self, player: "Player"):
        self.players.append(player)

    def next_round(self):
        # TODO 如果沒有下一局，丟 exception
        self.rounds.append(Round(deepcopy(self.players)))

    def to_dict(self):
        return dict(game_id=self.id, players=[x.to_dict() for x in self.players],
                    rounds=[x.to_dict() for x in self.rounds])

    def play(self, player_id: str, card_name: str, card_action: Union[GuessCard, ToSomeoneCard, None]):
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

    def handle_when_guess_card_action(self, player_id: str, card_name: str, action: GuessCard):
        if not isinstance(action, GuessCard):
            return

        turn_player: "Player" = self.find_player_by_id(player_id)
        opponent: "Player" = self.find_player_by_id(action.opponent)

        turn_player.play_opponent_two_cards(opponent,
                                            find_card_by_name(card_name),
                                            find_card_by_name(action.guess_card))

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


class Player:

    def __init__(self):
        self.name: str = None
        self.cards: List["Card"] = []
        self.am_i_out: bool = False
        self.protected = False
        self.total_value_of_card: int = 0

    def play_opponent_two_cards(
            self, opponent: "Player" = None, card_will_be_played: "Card" = None, with_card: "Card" = None
    ):
        # TODO precondition: the player must hold 2 cards
        if len(self.cards) != 2:
            return False

        # Check will_be_played_card is in the hands
        if not any([True for c in self.cards if c.name == card_will_be_played.name]):
            return False

        if card_will_be_played.can_not_play(self):
            return False

        if opponent and opponent.protected:
            # TODO send completed event for player
            return

        card_will_be_played.execute_with_card(opponent, with_card)

        # TODO postcondition: the player holds 1 card after played
        self.cards = list(filter(lambda x: x.name == card_will_be_played.name, self.cards))
        if len(self.cards) != 1:
            return False
        self.total_value_of_card += card_will_be_played.level

        return True

    def out(self):
        self.am_i_out = True

    def to_dict(self):
        return dict(name=self.name, out=self.am_i_out)
