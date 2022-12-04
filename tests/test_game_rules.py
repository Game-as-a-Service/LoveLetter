from typing import Callable
from unittest import TestCase

from love_letter.models import Game, GameException, Player


class GetGameStartedTests(TestCase):

    def setUp(self):
        self.exception: BaseException = None
        self.exception_message: str = None

    def catch(self, callable: Callable):
        with self.assertRaises(BaseException) as ex:
            callable()
        self.exception = ex.exception
        self.exception_message = str(ex.exception)

    def test_game_can_start_at_least_two_players(self):
        """
        遊戲至少需要 2 名玩家才可以開始
        """

        # given a new game
        game: Game = Game()

        # when we start it
        self.catch(lambda: game.start())

        # then get exception
        self.assertEqual("Too Few Players", self.exception_message)

        # when we add two players and start it
        game.join(Player.create('1'))
        game.join(Player.create('2'))
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
