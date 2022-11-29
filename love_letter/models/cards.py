import abc


class Card(metaclass=abc.ABCMeta):
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

    def execute_with_card(self, player: "Player", guessing_card: "Card"):
        for card in player.cards:
            if guessing_card == card:
                player.out()


class PriestCard(Card):
    name = '神父'
    level = 2


class BaronCard(Card):
    name = '男爵'
    level = 3


class PrinceCard(Card):
    name = '王子'
    level = 5

    def can_not_play(self, player: "Player"):
        return COUNTESS_CARD in player.cards


class KingCard(Card):
    name = '國王'
    level = 6

    def can_not_play(self, player: "Player"):
        return COUNTESS_CARD in player.cards


class CountessCard(Card):
    name = '伯爵夫人'
    level = 7

    def execute_with_card(self, player: "Player", card: "Card"):
        pass


class PrincessCard(Card):
    name = '公主'
    level = 8

    def execute_with_card(self, player: "Player", card: "Card"):
        player.out()


def find_card_by_name(name):
    for card in ALL_CARD_TYPES:
        if card.name == name:
            return card
    raise ValueError(f'Cannot find the card with name: {name}')


ALL_CARD_TYPES = [GuardCard(), PriestCard(), BaronCard(), PrinceCard(), KingCard(), CountessCard(), PrincessCard(), ]
COUNTESS_CARD = find_card_by_name("伯爵夫人")
