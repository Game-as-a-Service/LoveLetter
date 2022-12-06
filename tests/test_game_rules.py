from typing import Callable, List
from unittest import TestCase

from love_letter.models import Deck, Game, GameException, Player
from love_letter.web.dto import GuessCard


def reset_deck(card_name_list: List[str]):
    class _TestDeck(Deck):
        def shuffle(self, player_num: int):
            super().shuffle(player_num)
            from love_letter.models import find_card_by_name as c
            self.cards = [c(x) for x in card_name_list]

    import love_letter.models
    love_letter.models.deck_factory = lambda: _TestDeck()


class GetGameStartedTests(TestCase):

    def setUp(self):
        self.exception_message: str = None

    def catch(self, callable: Callable):
        with self.assertRaises(BaseException) as ex:
            callable()
        self.exception_message = str(ex.exception)

    def test_game_can_not_start_less_than_two_players(self):
        """
        遊戲不滿 2 名玩家無法開始
        """

        # given a new game
        game: Game = Game()

        # when we start it
        self.catch(lambda: game.start())

        # then get exception
        self.assertEqual("Too Few Players", self.exception_message)

    def test_game_can_start_at_least_two_players(self):
        """
        遊戲至少需要 2 名玩家才可以開始
        """

        # given a new game with two players
        game: Game = Game()
        game.join(Player.create('1'))
        game.join(Player.create('2'))

        # when starting the game
        game.start()

        # then the game has started
        self.assertTrue(game.has_started())

    def test_players_can_join_game_before_it_started(self):
        """
        一旦遊戲已經開始，玩家就無法再加入遊戲。
        """

        # given a started game
        game: Game = Game()
        game.join(Player.create('1'))
        game.join(Player.create('2'))
        game.start()

        # when a player join the started game
        self.catch(lambda: game.join(Player.create('3')))

        # then it got error
        self.assertEqual("Game Has Started", self.exception_message)

    def test_players_cannot_join_game_after_4th_player(self):
        """
        遊戲最多 4 個玩家，晚來的就不能加了。
        """

        # given a not started game with 4 players
        game: Game = Game()
        game.join(Player.create('1'))
        game.join(Player.create('2'))
        game.join(Player.create('3'))
        game.join(Player.create('4'))

        # when another player join the game
        self.catch(lambda: game.join(Player.create('5')))

        # then it got error
        self.assertEqual("Game Has No Capacity For New Players", self.exception_message)


class PlayingGameTests(TestCase):

    def setUp(self):
        # make a game with 3 players
        game: Game = Game()
        game.join(Player.create('1'))
        game.join(Player.create('2'))
        game.join(Player.create('3'))
        self.game: Game = game

    def test_after_game_start_every_player_get_1_card_and_turn_player_get_extra_1(self):
        """
        遊戲開始後，人人獲得一張手牌。
        turn player 會再多一張手牌
        """

        # given the arranged deck
        reset_deck([
            '王子',  # player 1
            '神父',  # player 2
            '公主',  # player 3
            '衛兵',  # turn player owns it
            '衛兵',
            '衛兵',
            '衛兵',
        ])

        # when start the arranged game
        self.game.start()

        # then player get the expected cards
        expected_card_mapping = [('1', ['王子', '衛兵']), ('2', ['神父']), ('3', ['公主'])]
        for index, player in enumerate(self.game.this_round_players()):
            name, cards = expected_card_mapping[index]
            self.assertEqual(name, player.name)
            self.assertEqual(cards, [x.name for x in player.cards])

    def test_shift_turn_player_one_by_one(self):
        """
        出牌後，完成觸發效果就換下一位。
        試著都沒有人出局的情況下，是否會輪回第 1 個玩家
        """

        # given the arranged deck (塞 1 百個衛兵在牌庫)
        reset_deck(list(['衛兵' for x in range(100)]))

        # given a started game
        self.game.start()

        # when 3 player discarded twice but nothing happened
        self.game.play('1', '衛兵', GuessCard(chosen_player='2', guess_card='公主'))
        self.game.play('2', '衛兵', GuessCard(chosen_player='3', guess_card='公主'))
        self.game.play('3', '衛兵', GuessCard(chosen_player='1', guess_card='公主'))
        self.game.play('1', '衛兵', GuessCard(chosen_player='2', guess_card='公主'))
        self.game.play('2', '衛兵', GuessCard(chosen_player='3', guess_card='公主'))
        self.game.play('3', '衛兵', GuessCard(chosen_player='1', guess_card='公主'))

        # then the game is still at round 1
        self.assertEqual(1, len(self.game.rounds))

        # then the turn player back to the player 1
        self.assertEqual('1', self.game.rounds[-1].turn_player.name)

        # then the turn player earns 2 points by discarding 衛兵 twice
        self.assertEqual(2, self.game.rounds[-1].turn_player.total_value_of_card)
