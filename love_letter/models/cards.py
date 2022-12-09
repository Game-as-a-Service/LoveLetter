import abc
import random
from typing import List

REJECT_BY_RULE = ValueError("You can not discard by the rule")


class Card(metaclass=abc.ABCMeta):
    """
    A card could be discarded by the turn-player or a chosen player who was assigned by the turn player.
    Either turn player or chosen player would take effect when the card is discarded.
    Sometimes, nothing happen, it just a discarded card by the turn player.


    There are some properties in a card:

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

    @abc.abstractmethod
    def trigger_effect(self, card_holder: "Player", chosen_player: "Player" = None, with_card: "Card" = None):
        """
        play the card to player with a card by rules

        Ex. the GuardCard needs to play with a card for guessing.

        purely play the card to player(can be opponent or myself)
        Ex. play priest_card to the other opponent.
        Ex. play handmaid_card to myself.
        Ex. play king_card to the other opponent.
        """
        return NotImplemented

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self) -> str:
        return str(f"Card({self.name},{self.value})")


class GuardCard(Card):
    name = '衛兵'
    value = 1
    quantity = 5

    def trigger_effect(self, card_holder: "Player", chosen_player: "Player" = None, with_card: "Card" = None):
        for card in chosen_player.cards:
            if with_card == card:
                chosen_player.out()
                break


class PriestCard(Card):
    name = '神父'
    value = 2
    quantity = 2

    def trigger_effect(self, card_holder: "Player", chosen_player: "Player" = None, with_card: "Card" = None):
        from love_letter.models import Seen
        seen_card = Seen(chosen_player.name, chosen_player.cards[-1])
        card_holder.seen_cards.append(seen_card)


class BaronCard(Card):
    name = '男爵'
    value = 3
    quantity = 2

    def trigger_effect(self, card_holder: "Player", chosen_player: "Player" = None, with_card: "Card" = None):
        raise NotImplemented


class HandmaidCard(Card):
    name = '侍女'
    value = 4
    quantity = 2

    def trigger_effect(self, card_holder: "Player", chosen_player: "Player" = None, with_card: "Card" = None):
        card_holder.protected = True


class PrinceCard(Card):
    name = '王子'
    value = 5
    quantity = 2

    """
    When you discard Prince Arnaud, choose one player still in the round (including yourself). 
    That player discards his or her hand (do not apply its effect) and draws a new card. 
    If the deck is empty, that player draws the card that was removed at the start of the round
    """

    def trigger_effect(self, card_holder: "Player", chosen_player: "Player" = None, with_card: "Card" = None):
        # choose self to discard the card in the hand
        for c in card_holder.cards:
            if c.name == "伯爵夫人":
                raise REJECT_BY_RULE

        for card in chosen_player.cards:
            if "公主" == card.name:
                chosen_player.out()

        # TODO the game system should send a new card to the player who did discard
        chosen_player.cards = []


class KingCard(Card):
    name = '國王'
    value = 6
    quantity = 1

    def trigger_effect(self, card_holder: "Player", chosen_player: "Player" = None, with_card: "Card" = None):
        for c in card_holder.cards:
            if c.name == "伯爵夫人":
                raise REJECT_BY_RULE

        # 出牌者剩下的牌(型別為list)
        card_holder_left_card = list(filter(lambda x: x.name != self.name, card_holder.cards))
        # 因為出牌者剩下的牌list只有一個元素，故直接寫[0]
        card_holder_swap_card_index = card_holder.cards.index(card_holder_left_card[0])
        chosen_player.cards[0], card_holder.cards[card_holder_swap_card_index] =\
            card_holder.cards[card_holder_swap_card_index], chosen_player.cards[0]



class CountessCard(Card):
    name = '伯爵夫人'
    value = 7
    quantity = 1

    """
    Unlike other cards, which take effect when discarded, the text on the Countess applies while she is in your hand. 
    In fact, she has no effect when you discard her.

    If you ever have the Countess and either the King or Prince in your hand, 
    you must discard the Countess. You do not have to reveal the other card in your hand. 
    Of course, you can also discard the Countess even if you do not have a royal family member in your hand. 
    She likes to play mind games....
    """

    def trigger_effect(self, card_holder: "Player", chosen_player: "Player" = None, with_card: "Card" = None):
        # nothing happen by the rule
        pass


class PrincessCard(Card):
    name = '公主'
    value = 8
    quantity = 1

    def trigger_effect(self, card_holder: "Player", chosen_player: "Player" = None, with_card: "Card" = None):
        card_holder.out()


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

    def draw(self, player: "Player") -> bool:
        """
        Player draw the top card.
        :param player:
        :return:
        """
        if len(self.cards) == 0:
            return False
        player.cards.append(self.cards.pop(0))
        return True


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
