import unittest

from love_letter.models import Player
from love_letter.models.cards import find_card_by_value

player1 = Player().create("Player 1")
player2 = Player().create("Player 2")
player3 = Player().create("Player 3")


def assign_values(player: Player, value: int, total_value: int):
    player.cards = [find_card_by_value(value)]
    player.total_value_of_card = total_value


class PlayersTest(unittest.TestCase):
    def setUp(self) -> None:
        self.players = [player1, player2, player3]

    def test_compare_hand_card(self):
        assign_values(player1, 4, 10)
        assign_values(player2, 6, 3)
        assert player1 < player2

    def test_compare_total_value_if_tie(self):
        assign_values(player1, 4, 10)
        assign_values(player2, 4, 3)
        assert player1 > player2

    def test_find_winner(self):
        assign_values(player1, 3, 10)
        assign_values(player2, 6, 3)
        assign_values(player3, 6, 7)
        assert max([player1, player2, player3]) == player3

    def test_unable_to_compare(self):
        player1.cards = [find_card_by_value(2), find_card_by_value(1)]
        assign_values(player2, 6, 3)

        def compare():
            return player1 > player2

        self.assertRaises(AssertionError, compare)
