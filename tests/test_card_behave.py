import unittest
from typing import List, Optional

# isort: off
from love_letter.models import Deck, Game, GuessCard, Player, Round, ToSomeoneCard


# isort: on


class _TestDeckForCardBehave(Deck):
    def __init__(self, card_name_list, reset_remove_by_rule_cards):
        self.card_name_list = card_name_list
        self.reset_remove_by_rule_cards = reset_remove_by_rule_cards

    def shuffle(self, player_num: int):
        super().shuffle(player_num)
        from love_letter.models import find_card_by_name as c

        self.cards = [c(x) for x in self.card_name_list]
        self.remove_by_rule_cards = (
            [c(x) for x in self.reset_remove_by_rule_cards]
            if self.reset_remove_by_rule_cards is not None
            else []
        )


def reset_deck(
    card_name_list: List[str], remove_by_rule_cards: Optional[List[str]] = None
):
    import love_letter.models

    love_letter.models.deck_factory = lambda: _TestDeckForCardBehave(
        card_name_list, remove_by_rule_cards
    )


class LoseHandMaidProtected(unittest.TestCase):
    def setUp(self) -> None:
        self.game: Game = Game()
        self.game.join(Player("1"))
        self.game.join(Player("2"))

        # disable random-picker for the first round
        # it always returns the first player
        self.origin_choose_one_randomly = Round.choose_one_randomly
        Round.choose_one_randomly = lambda players: players[0]

    def tearDown(self) -> None:
        Round.choose_one_randomly = self.origin_choose_one_randomly

    def test_finish_one_round_lose_handmaid_protected(self):
        """
        遊戲開始後，經過一輪後玩家1失去侍女保護，可以被其他玩家執行卡牌效果
        玩家1 出牌 獲得侍女保護
        玩家2 對 玩家1 出牌 衛兵 指定 公主 => 玩家1 被侍女保護 無效
        玩家1 出牌 伯爵夫人
        玩家2 對 玩家1 出牌 衛兵 指定 公主 => 玩家1 出局
        :return:
        """

        # given the arranged deck
        reset_deck(["侍女", "神父", "公主", "衛兵", "伯爵夫人", "衛兵"])

        # given a started game
        self.game.start()

        self.game.play("1", "侍女", None)  # player-1 was protected

        # then player-1 was protected
        self.assertTrue(self.game.this_round_players()[0].protected)

        self.game.play(
            "2",
            "衛兵",  # player-2 can't kill player-1, because player-1 was protected
            GuessCard(chosen_player="1", guess_card="公主"),
        )

        # then player-1 lose protected
        self.assertFalse(self.game.this_round_players()[0].protected)

        self.game.play("1", "伯爵夫人", None)  # player-1 lose protected
        self.game.play(
            "2",
            "衛兵",  # player-2 can kill player-1
            GuessCard(chosen_player="1", guess_card="公主"),
        )

        # then the player-2 will be
        # 1. the winner of the last round
        # 2. the turn player at the new round
        self.assertEqual(2, len(self.game.rounds))  # there are two rounds
        self.assertEqual("2", self.game.rounds[-2].winner)  # the last round winner
        self.assertEqual(
            "2", self.game.get_turn_player().name
        )  # turn player of this round


# 捨棄王子抽取移除卡片的規則
class DiscardPrinceCardTests(unittest.TestCase):
    def setUp(self) -> None:
        self.game: Game = Game()
        self.game.join(Player("1"))
        self.game.join(Player("2"))

        # disable random-picker for the first round
        # it always returns the first player
        self.origin_choose_one_randomly = Round.choose_one_randomly
        Round.choose_one_randomly = lambda players: players[0]

    def tearDown(self) -> None:
        Round.choose_one_randomly = self.origin_choose_one_randomly

    def test_discard_prince_card_and_chosen_player_get_other_card_from_deck(self):
        """
        測試出王子牌，系統從牌庫補牌
        玩家A 對 玩家B 出牌 王子，玩家B 棄牌後系統補發一張給 玩家B
        :return:
        """

        # given the arranged deck
        reset_deck(["王子", "男爵", "國王", "衛兵", "衛兵"])

        # given a started game
        self.game.start()

        # when player-1 discards the prince and chosen player-2
        self.game.play("1", "王子", ToSomeoneCard(chosen_player="2"))

        # then player-2 is turn player, so have two card in hands
        self.assertEqual(len(self.game.get_turn_player().cards), 2)

        # then the deck is empty
        self.assertEqual(len(self.game.rounds[-1].deck.cards), 0)

    def test_discard_prince_card_and_chosen_player_out_and_not_get_other_card_from_deck(
        self,
    ):
        """
        測試出王子牌，系統不從牌庫補牌，因為玩家已經出局
        玩家A 對 玩家B 出牌 王子，玩家B棄牌公主，該局結束，系統不發牌
        :return:
        """

        # given the arranged deck
        reset_deck(["王子", "公主", "國王", "衛兵", "衛兵"])

        # given a started game
        self.game.start()

        # when player-1 discards the prince and chosen player-2
        self.game.play("1", "王子", ToSomeoneCard(chosen_player="2"))

        # then player-2 is out and don't have card in hands
        self.assertEqual(self.game.rounds[-2].winner, "1")

        # then player get the expected cards
        expected_card_mapping = [("1", ["國王"]), ("2", [])]
        for index, player in enumerate(self.game.rounds[-2].players):
            name, cards = expected_card_mapping[index]
            self.assertEqual(name, player.name)
            self.assertEqual(cards, [x.name for x in player.cards])

    def test_discard_prince_card_and_chosen_player_get_other_card_from_deck_and_deck_card_is_empty(
        self,
    ):
        """
        測試出王子牌，系統從牌庫補牌，補完牌後牌庫也沒牌 => 遊戲結束
        玩家A 對 玩家B 出牌 王子，玩家B 棄牌後系統補發一張給 玩家B
        :return:
        """

        # given the arranged deck
        reset_deck(["王子", "男爵", "國王", "衛兵"])

        # given a started game
        self.game.start()

        # when player-1 discards the prince and chosen player-2
        self.game.play("1", "王子", ToSomeoneCard(chosen_player="2"))

        # then player-2 has one card from deck card in the last round
        self.assertEqual(len(self.game.get_turn_player(-2).cards), 1)

        # then player-1 is the winner
        self.assertEqual(self.game.rounds[-2].winner, "1")

        # then the last round deck is empty
        self.assertEqual(len(self.game.rounds[-2].deck.cards), 0)

    def test_discard_prince_card_and_chosen_player_get_other_card_from_remove_by_rule_card(
        self,
    ):
        """
        測試出王子牌，牌庫沒牌補，系統把剩餘牌拿去補牌
        :return:
        """
        # given the arranged deck
        reset_deck(["王子", "男爵", "國王"], ["衛兵"])

        # given a started game
        self.game.start()

        # when player-1 discards the prince and chosen player-2
        self.game.play("1", "王子", ToSomeoneCard(chosen_player="2"))

        # then player-2 has one card from deck remove_by_rule_cards in the last round
        self.assertEqual(len(self.game.get_turn_player(-2).cards), 1)

        # then player-1 is the winner
        self.assertEqual(self.game.rounds[-2].winner, "1")

        # then the deck cards is empty in last round
        self.assertEqual(len(self.game.rounds[-2].deck.cards), 0)

        # then the deck remove_by_rule_card is empty in last round
        self.assertEqual(len(self.game.rounds[-2].deck.remove_by_rule_cards), 0)


class DiscardBaronCardTests(unittest.TestCase):
    def setUp(self) -> None:
        self.game: Game = Game()
        self.game.join(Player("1"))
        self.game.join(Player("2"))

        # disable random-picker for the first round
        # it always returns the first player
        self.origin_choose_one_randomly = Round.choose_one_randomly
        Round.choose_one_randomly = lambda players: players[0]

    def tearDown(self) -> None:
        Round.choose_one_randomly = self.origin_choose_one_randomly

    def test_retire_opponent_if_greater_hand_card_value(self):
        """
        遊戲開始後，經過一輪後玩家1抽得男爵
        玩家1 出牌 男爵，指定玩家2
        玩家1 與 玩家2 比較手牌 => 玩家2 出局
        :return:
        """

        # given the arranged deck
        reset_deck(["國王", "神父", "男爵"])

        # given a started game
        self.game.start()

        self.game.play("1", "男爵", ToSomeoneCard(chosen_player="2"))
        # King (6) is larger than Priest (2). Player-1 won.
        self.assertEqual(self.game.rounds[-2].winner, "1")

    def test_retire_self_if_smaller_hand_card_value(self):
        """
        遊戲開始後，經過一輪後玩家1抽得男爵
        玩家1 出牌 男爵，指定玩家2
        玩家1 與 玩家2 比較手牌 => 玩家1 出局
        :return:
        """

        # given the arranged deck
        reset_deck(["神父", "國王", "男爵"])

        # given a started game
        self.game.start()

        self.game.play("1", "男爵", ToSomeoneCard(chosen_player="2"))
        # King (6) is larger than Priest (2). Player-2 won.
        self.assertEqual(self.game.rounds[-2].winner, "2")

    def test_if_equal_hand_card_value(self):
        """
        遊戲開始後，經過一輪後玩家1抽得男爵
        玩家1 出牌 男爵，指定玩家2
        玩家1 與 玩家2 比較手牌 => 手牌相等 此局繼續
        玩家2 出牌 衛兵，指定玩家1，正確猜測手牌 => 玩家1 出局
        :return:
        """

        # given the arranged deck
        reset_deck(["神父", "神父", "男爵", "衛兵"])

        # given a started game
        self.game.start()

        # 手牌相等，無人出局，此局繼續
        self.game.play("1", "男爵", ToSomeoneCard(chosen_player="2"))
        for player in self.game.players:
            self.assertEqual(player.am_i_out, False)


class EndRoundTests(unittest.TestCase):
    def setUp(self) -> None:
        self.game: Game = Game()
        self.game.join(Player("1"))
        self.game.join(Player("2"))

        # disable random-picker for the first round
        # it always returns the first player
        self.origin_choose_one_randomly = Round.choose_one_randomly
        Round.choose_one_randomly = lambda x: x[0]

    def tearDown(self) -> None:
        Round.choose_one_randomly = self.origin_choose_one_randomly

    def test_left_one_player_winner_get_token_of_affection(self):
        """
        遊戲開始後，剩餘一位玩家，此局結束，勝者拿到一枚好感指示物
        玩家1 對 玩家2 出牌 衛兵 指定 神父 => 玩家2 出局
        此局結束 玩家1 獲得一枚好感指示物
        :return:
        """

        # given the arranged deck
        reset_deck(["衛兵", "神父", "公主", "衛兵", "伯爵夫人", "衛兵"])

        # given a started game
        self.game.start()

        # when only one player left
        self.game.play(
            "1",
            "衛兵",  # player1 guess card correctly
            GuessCard(chosen_player="2", guess_card="神父"),
        )

        # then player1 gets 1 token of affection in both game class and round class
        self.assertEqual(1, self.game.players[0].tokens_of_affection)
        self.assertEqual(1, self.game.rounds[-2].players[0].tokens_of_affection)
        # then the player-1 will be
        # 1. the winner of the last round
        # 2. the turn player at the new round
        self.assertEqual(2, len(self.game.rounds))  # there are two rounds
        self.assertEqual("1", self.game.rounds[-2].winner)  # the last round winner
        self.assertEqual(
            "1", self.game.rounds[-1].turn_player.name
        )  # turn player of this round

    def test_with_no_card_in_deck_the_player_has_biggest_card_is_the_winner(self):
        """
        遊戲開始後，牌庫的牌抽完，此局結束，手牌較大者獲勝，勝者拿到一枚好感指示物
        玩家1 出牌 獲得侍女保護
        此局結束 玩家2手牌較大 獲得一枚好感指示物
        :return:
        """

        # given the arranged deck
        reset_deck(["衛兵", "神父", "侍女"])

        # given a started game
        self.game.start()

        # when there is no card in deck, compare player's card
        self.game.play("1", "侍女", None)

        # then player2 gets 1 token of affection in both game class and round class
        self.assertEqual(1, self.game.players[1].tokens_of_affection)
        self.assertEqual(1, self.game.rounds[-2].players[1].tokens_of_affection)
        # then the player-2 will be
        # 1. the winner of the last round
        # 2. the turn player at the new round
        self.assertEqual(2, len(self.game.rounds))  # there are two rounds
        self.assertEqual("2", self.game.rounds[-2].winner)  # the last round winner
        self.assertEqual(
            "2", self.game.rounds[-1].turn_player.name
        )  # turn player of this round

    def test_with_no_card_in_deck_more_than_one_player_has_biggest_card(self):
        """
        遊戲開始後，牌庫的牌抽完，此局結束，手牌較大者獲勝，手牌較大的玩家有兩位以上時，比較棄牌堆大小，勝者拿到一枚好感指示物
        玩家1 出牌 獲得侍女保護
        此局結束 玩家1的棄牌堆總和較大 獲得一枚好感指示物
        :return:
        """

        # given the arranged deck
        reset_deck(["神父", "神父", "侍女"])

        # given a started game
        self.game.start()

        # when there is no card in deck, compare player's card
        # when two or more than two player have the biggest card in hand, compare the total_value_of_card
        self.game.play("1", "侍女", None)

        # then player2 gets 1 token of affection in both game class and round class
        self.assertEqual(1, self.game.players[0].tokens_of_affection)
        self.assertEqual(1, self.game.rounds[-2].players[0].tokens_of_affection)
        # then the player-1 will be
        # 1. the winner of the last round
        # 2. the turn player at the new round
        self.assertEqual(2, len(self.game.rounds))  # there are two rounds
        self.assertEqual("1", self.game.rounds[-2].winner)  # the last round winner
        self.assertEqual(
            "1", self.game.rounds[-1].turn_player.name
        )  # turn player of this round


class EndGameTest(unittest.TestCase):
    def setUp(self) -> None:
        self.game: Game = Game()
        self.game.join(Player("1"))
        self.game.join(Player("2"))

        # disable random-picker for the first round
        # it always returns the first player
        self.origin_choose_one_randomly = Round.choose_one_randomly
        Round.choose_one_randomly = lambda x: x[0]

    def tearDown(self) -> None:
        Round.choose_one_randomly = self.origin_choose_one_randomly

    def test_with_no_card_in_deck_more_than_one_player_has_biggest_card(self):
        """
        遊戲開始後，牌庫的牌抽完，此局結束，手牌較大者獲勝，手牌較大的玩家有兩位以上時，比較棄牌堆大小，勝者拿到一枚好感指示物
        玩家1 出牌 獲得侍女保護
        此局結束 玩家1的棄牌堆總和較大 獲得一枚好感指示物
        :return:
        """

        # given the arranged deck
        reset_deck(["神父", "神父", "侍女"])

        # given a started game
        self.game.start()

        for _ in range(7):
            # when there is no card in deck, compare player's card
            # when two or more than two player have the biggest card in hand, compare the total_value_of_card
            self.game.play("1", "侍女", None)

        # then player1 gets 7 token of affection
        self.assertEqual(7, self.game.players[0].tokens_of_affection)
        # then there are 7 rounds in total
        self.assertEqual(7, len(self.game.rounds))  # there are seven rounds
        # then the player-1 will be the winner
        self.assertEqual("1", self.game.final_winner)  # the last round winner
