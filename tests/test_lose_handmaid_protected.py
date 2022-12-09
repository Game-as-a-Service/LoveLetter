import unittest
from typing import List

from love_letter.models import Deck, Game, Player
from love_letter.web.dto import GuessCard


def reset_deck(card_name_list: List[str]):
    class _TestDeck(Deck):
        def shuffle(self, player_num: int):
            super().shuffle(player_num)
            from love_letter.models import find_card_by_name as c
            self.cards = [c(x) for x in card_name_list]

    import love_letter.models
    love_letter.models.deck_factory = lambda: _TestDeck()


class LoseHandMaidProtected(unittest.TestCase):
    def setUp(self) -> None:
        self.game: Game = Game()
        self.game.join(Player.create('1'))
        self.game.join(Player.create('2'))

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
