import unittest

from love_letter.models import Player
from love_letter.models.cards import Deck

TOTAL_CARDS_NUMBER = 16
PLAYER_NUM_OF_CARD_NUM = [
    dict(player_num=2, cards_num=13, remove_cards_num=3),
    dict(player_num=3, cards_num=15, remove_cards_num=1),
    dict(player_num=4, cards_num=15, remove_cards_num=1),
]


class DeckTest(unittest.TestCase):
    def setUp(self) -> None:
        self.deck = Deck()

    def test_shuffle_with_different_number_of_players(self):
        for info in PLAYER_NUM_OF_CARD_NUM:
            self.deck.shuffle(info["player_num"])
            assert len(self.deck.cards) == info["cards_num"]
            assert len(self.deck.remove_by_rule_cards) == info["remove_cards_num"]
            assert (
                len(self.deck.cards + self.deck.remove_by_rule_cards)
                == TOTAL_CARDS_NUMBER
            )

    def test_player_draw(self):
        player_num = 2
        players = [Player(str(i)) for i in range(player_num)]

        self.deck.shuffle(player_num)

        for player in players:
            self.deck.draw_card(player)
            assert len(player.cards) == 1
