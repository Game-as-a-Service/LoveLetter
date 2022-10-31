import abc


class Card(metaclass=abc.ABCMeta):

    def execute_with_card(self, player: "Player", card: "Card"):
        """
        play the card to player with a card by rules

        Ex. the GuardCard needs to play with a card for guessing.
        """
        return NotImplemented


class GuardCard(Card):
    name = '衛兵'

    def execute_with_card(self, player: "Player", guessing_card: "Card"):
        for card in player.cards:
            if guessing_card == card:
                player.out()


class PriestCard(Card):
    name = '牧師'


class BaronCard(Card):
    name = '男爵'


class PrincessCard(Card):
    name = '公主'


all_card_types = [GuardCard(), PriestCard(), BaronCard(), PrincessCard()]


def find_card_by_name(name):
    for card in all_card_types:
        if card.name == name:
            return card
    raise ValueError(f'Cannot find the card with name: {name}')
