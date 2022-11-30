import random
from typing import List

from love_letter.models.cards import PrincessCard, GuardCard, PriestCard, BaronCard, HandmaidCard, PrinceCard, \
    KingCard, CountessCard


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

        for card, num in CARDS_OF_NUM.items():
            self.cards.extend([card() for _ in range(num)])

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


CARDS_OF_NUM = [
    dict(
        card=GuardCard,
        num=5
    ),
    dict(
        card=PriestCard,
        num=2
    ),
    dict(
        card=BaronCard,
        num=2
    ),
    dict(
        card=HandmaidCard,
        num=2
    ),
    dict(
        card=PrinceCard,
        num=2
    ),
    dict(
        card=KingCard,
        num=1
    ),
    dict(
        card=CountessCard,
        num=1
    ),
    dict(
        card=PrincessCard,
        num=1
    ),
]
CARDS_OF_NUM = {card_info["card"]: card_info["num"] for card_info in CARDS_OF_NUM}
