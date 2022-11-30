import abc


class Card(metaclass=abc.ABCMeta):
    """
    There are some properties in a card

    +---------+----------+
    | Level   | Name     |
    +---------+----------+
    | Picture            | * Quantity
    +--------------------+
    | Effect Description |
    +--------------------+


    * level: how intimate is this card with the princess
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
    level = 1
    number = 5

    def execute_with_card(self, player: "Player", guessing_card: "Card"):
        for card in player.cards:
            if guessing_card == card:
                player.out()


class PriestCard(Card):
    name = '神父'
    level = 2
    number = 2


class BaronCard(Card):
    name = '男爵'
    level = 3
    number = 2


class HandmaidCard(Card):
    name = '侍女'
    level = 4
    number = 2


class PrinceCard(Card):
    name = '王子'
    level = 5
    number = 2

    def can_not_play(self, player: "Player"):
        return COUNTESS_CARD in player.cards

    def execute_with_card(self, player: "Player", card: "Card"):
        for card in player.cards:
            if "公主" == card.name:
                player.out()
        player.cards = []


class KingCard(Card):
    name = '國王'
    level = 6
    number = 1

    def can_not_play(self, player: "Player"):
        return COUNTESS_CARD in player.cards


class CountessCard(Card):
    name = '伯爵夫人'
    level = 7
    number = 1

    def execute_with_card(self, player: "Player", card: "Card"):
        pass


class PrincessCard(Card):
    name = '公主'
    level = 8
    number = 1

    def execute_with_card(self, player: "Player", card: "Card"):
        player.out()


def find_card_by_name(name):
    for card in ALL_CARD_TYPES:
        if card.name == name:
            return card
    raise ValueError(f'Cannot find the card with name: {name}')


ALL_CARD_TYPES = [
    GuardCard(), PriestCard(), BaronCard(),
    HandmaidCard(), PrinceCard(), KingCard(),
    CountessCard(), PrincessCard(),
]
COUNTESS_CARD = find_card_by_name("伯爵夫人")
