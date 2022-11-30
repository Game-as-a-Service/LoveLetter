import random
from typing import List

from love_letter.models.cards import ALL_CARD_TYPES


class Deck:
    def __init__(self):
        self.cards: List["Card"] = []
        self.remove_by_rule_cards: List["Card"] = []

    def shuffle(self, player_num: int):
        """
        Reset deck cards and remove rule cards.
        :param player_num: 2 ~ 4
        :return:
        """
        self.cards = []
        self.remove_by_rule_cards = []

        if player_num == 2:
            remove_cards_num = 3
        elif player_num in [3, 4]:
            remove_cards_num = 1
        else:
            raise ValueError("player number is not support")

        for card in ALL_CARD_TYPES:
            self.cards.extend([card for _ in range(card.number)])

        random.shuffle(self.cards)
        random.shuffle(self.cards)

        for num in range(remove_cards_num):
            self.remove_by_rule_cards.append(self.cards.pop(0))

    def draw(self, player: "Player"):
        """
        Player draw the top card.
        :param player:
        :return:
        """
        player.cards.append(self.cards.pop(0))
