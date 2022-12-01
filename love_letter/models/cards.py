import abc
import random
from typing import List


class Card(metaclass=abc.ABCMeta):
    """
    There are some properties in a card

    +---------+----------+
    | Value   | Name     |
    +---------+----------+
    | Picture | Quantity |
    +--------------------+
    | Effect Description |
    +--------------------+

    * value: how intimate is this card with the princess
    * name: the name of this card
    * (not yet planned) picture:
    * (not yet planned) description: the effect of this card
    * quantity: how many copies of this card

    """

    def can_not_play(self, player: "Player"):
        return False

    def execute_with_card(self, player: "Player", card: "Card"):
        """
        play the card to player with a card by rules

        Ex. the GuardCard needs to play with a card for guessing.
        """
        return NotImplemented

    def __eq__(self, other):
        return self.name == other.name


class GuardCard(Card):
    name = '衛兵'
    value = 1
    quantity = 5

    def execute_with_card(self, player: "Player", guessing_card: "Card"):
        for card in player.cards:
            if guessing_card == card:
                player.out()


class PriestCard(Card):
    name = '神父'
    value = 2
    quantity = 2


class BaronCard(Card):
    name = '男爵'
    value = 3
    quantity = 2


class HandmaidCard(Card):
    name = '侍女'
    value = 4
    quantity = 2


class PrinceCard(Card):
    name = '王子'
    value = 5
    quantity = 2

    def can_not_play(self, player: "Player"):
        return COUNTESS_CARD in player.cards

    def execute_with_card(self, player: "Player", card: "Card"):
        for card in player.cards:
            if "公主" == card.name:
                player.out()
        player.cards = []


class KingCard(Card):
    name = '國王'
    value = 6
    quantity = 1

    def can_not_play(self, player: "Player"):
        return COUNTESS_CARD in player.cards


class CountessCard(Card):
    name = '伯爵夫人'
    value = 7
    quantity = 1

    def execute_with_card(self, player: "Player", card: "Card"):
        pass


class PrincessCard(Card):
    name = '公主'
    value = 8
    quantity = 1

    def execute_with_card(self, player: "Player", card: "Card"):
        player.out()


def find_card_by_name(name):
    for card in ALL_CARD_TYPES:
        if card.name == name:
            return card
    raise ValueError(f'Cannot find the card with name: {name}')


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
            self.cards.extend([card for _ in range(card.quantity)])

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


ALL_CARD_TYPES = [
    GuardCard(),
    PriestCard(),
    BaronCard(),
    HandmaidCard(),
    PrinceCard(),
    KingCard(),
    CountessCard(),
    PrincessCard(),
]
COUNTESS_CARD = find_card_by_name("伯爵夫人")
