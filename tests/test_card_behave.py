import unittest
from typing import List

from love_letter.models import Deck, Game, Player, Round
from love_letter.web.dto import GuessCard, ToSomeoneCard


def reset_deck(card_name_list: List[str], remove_by_rule_cards: List[str] = None):
    if remove_by_rule_cards is None:
        remove_by_rule_cards = []

    class _TestDeck(Deck):
        def shuffle(self, player_num: int):
            super().shuffle(player_num)
            from love_letter.models import find_card_by_name as c
            self.cards = [c(x) for x in card_name_list]
            self.remove_by_rule_cards = [c(x) for x in remove_by_rule_cards]

    import love_letter.models
    love_letter.models.deck_factory = lambda: _TestDeck()


class LoseHandMaidProtected(unittest.TestCase):
    def setUp(self) -> None:
        self.game: Game = Game()
        self.game.join(Player('1'))
        self.game.join(Player('2'))

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
        reset_deck(['侍女', '神父', '公主', '衛兵', '伯爵夫人', '衛兵'])

        # given a started game
        self.game.start()

        self.game.play("1", '侍女', None)  # player-1 was protected

        # then player-1 was protected
        self.assertTrue(self.game.this_round_players()[0].protected)

        self.game.play("2", '衛兵',  # player-2 can't kill player-1, because player-1 was protected
                       GuessCard(chosen_player='1', guess_card="公主"))

        # then player-1 lose protected
        self.assertFalse(self.game.this_round_players()[0].protected)

        self.game.play("1", '伯爵夫人', None)  # player-1 lose protected
        self.game.play("2", '衛兵',  # player-2 can kill player-1
                       GuessCard(chosen_player='1', guess_card="公主"))

        # then the player-2 will be
        # 1. the winner of the last round
        # 2. the turn player at the new round
        self.assertEqual(2, len(self.game.rounds))  # there are two rounds
        self.assertEqual('2', self.game.rounds[-2].winner)  # the last round winner
        self.assertEqual('2', self.game.rounds[-1].turn_player.name)  # turn player of this round


# 捨棄王子抽取移除卡片的規則
class DiscardPrinceCardTests(unittest.TestCase):
    def setUp(self) -> None:
        self.game: Game = Game()
        self.game.join(Player('1'))
        self.game.join(Player('2'))

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
        reset_deck(['王子', '男爵', '國王', '衛兵', '衛兵'])

        # given a started game
        self.game.start()

        # when player-1 discards the prince and chosen player-2
        self.game.play("1", "王子", ToSomeoneCard(chosen_player="2"))

        # then player-2 is turn player, so have two card in hands
        self.assertEqual(len(self.game.rounds[-1].turn_player.cards), 2)

        # then the deck is empty
        self.assertEqual(len(self.game.rounds[-1].deck.cards), 0)

    def test_discard_prince_card_and_chosen_player_out_and_not_get_other_card_from_deck(self):
        """
        測試出王子牌，系統不從牌庫補牌，因為玩家已經出局
        玩家A 對 玩家B 出牌 王子，玩家B棄牌公主，該局結束，系統不發牌
        :return:
        """

        # given the arranged deck
        reset_deck(['王子', '公主', '國王', '衛兵', '衛兵'])

        # given a started game
        self.game.start()

        # when player-1 discards the prince and chosen player-2
        self.game.play("1", "王子", ToSomeoneCard(chosen_player="2"))

        # then player-2 is out and don't have card in hands
        self.assertEqual(self.game.rounds[-2].winner, "1")

        # then player get the expected cards
        expected_card_mapping = [('1', ['國王']), ('2', [])]
        for index, player in enumerate(self.game.rounds[-2].players):
            name, cards = expected_card_mapping[index]
            self.assertEqual(name, player.name)
            self.assertEqual(cards, [x.name for x in player.cards])

    def test_discard_prince_card_and_chosen_player_get_other_card_from_deck_and_deck_card_is_empty(self):
        """
        測試出王子牌，系統從牌庫補牌，補完牌後牌庫也沒牌 => 遊戲結束
        玩家A 對 玩家B 出牌 王子，玩家B 棄牌後系統補發一張給 玩家B
        :return:
        """

        # given the arranged deck
        reset_deck(['王子', '男爵', '國王', '衛兵'])

        # given a started game
        self.game.start()

        # when player-1 discards the prince and chosen player-2
        self.game.play("1", "王子", ToSomeoneCard(chosen_player="2"))

        # then player-2 has one card from deck card in the last round
        self.assertEqual(len(self.game.rounds[-2].turn_player.cards), 1)

        # then player-1 is the winner
        self.assertEqual(self.game.rounds[-2].winner, "1")

        # then the last round deck is empty
        self.assertEqual(len(self.game.rounds[-2].deck.cards), 0)

    def test_discard_prince_card_and_chosen_player_get_other_card_from_remove_by_rule_card(self):
        """
        測試出王子牌，牌庫沒牌補，系統把剩餘牌拿去補牌
        :return:
        """
        # given the arranged deck
        reset_deck(['王子', '男爵', '國王'], ['衛兵'])

        # given a started game
        self.game.start()

        # when player-1 discards the prince and chosen player-2
        self.game.play("1", "王子", ToSomeoneCard(chosen_player="2"))

        # then player-2 has one card from deck remove_by_rule_cards in the last round
        self.assertEqual(len(self.game.rounds[-2].turn_player.cards), 1)

        # then player-1 is the winner
        self.assertEqual(self.game.rounds[-2].winner, "1")

        # then the deck cards is empty in last round
        self.assertEqual(len(self.game.rounds[-2].deck.cards), 0)

        # then the deck remove_by_rule_card is empty in last round
        self.assertEqual(len(self.game.rounds[-2].deck.remove_by_rule_cards), 0)


class DiscardBaronCardTests(unittest.TestCase):
    def setUp(self) -> None:
        self.game: Game = Game()
        self.game.join(Player('1'))
        self.game.join(Player('2'))

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
        reset_deck(['國王', '神父', '男爵'])

        # given a started game
        self.game.start()

        self.game.play("1", '男爵', ToSomeoneCard(chosen_player='2'))
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
        reset_deck(['神父', '國王', '男爵'])

        # given a started game
        self.game.start()

        self.game.play("1", '男爵', ToSomeoneCard(chosen_player='2'))
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
        reset_deck(['神父', '神父', '男爵', '衛兵'])

        # given a started game
        self.game.start()

        # 手牌相等，無人出局，此局繼續
        self.game.play("1", '男爵', ToSomeoneCard(chosen_player='2'))
        for player in self.game.players:
            self.assertEqual(player.am_i_out, False)
