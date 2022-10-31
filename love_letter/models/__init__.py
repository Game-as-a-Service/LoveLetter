from typing import List


class Player:

    def __init__(self):
        self.name: str = None
        self.cards: List["Card"] = []
        self.am_i_out: bool = False

    def play_opponent_two_cards(self, opponent: "Player", card_will_be_played: "Card", with_card: "Card"):
        # TODO precondition: the player must hold 2 cards
        self.cards = filter(lambda x: x.name == card_will_be_played.name, self.cards)

        card_will_be_played.execute_with_card(opponent, with_card)

        # TODO postcondition: the player holds 1 card after played
        pass

    def out(self):
        self.am_i_out = True
