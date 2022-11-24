from typing import List


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
