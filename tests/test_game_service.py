import json
import unittest

from love_letter.models import Player
from love_letter.repository import GameRepositoryInMemoryImpl
from love_letter.service import GameService
from love_letter.web.dto import GameStatus


class GameServiceTests(unittest.TestCase):

    def test_create_and_join_game(self):
        service = GameService(GameRepositoryInMemoryImpl())

        # create a new game
        game_id = service.create_game(Player.create("1").name)
        self.assertIsNotNone(game_id)

        # join the second player
        self.assertTrue(service.join_game(game_id, Player.create("2").name))
        result = service.get_status(game_id, '1')

        # # check the game status
        self.assertEqual(game_id, result.get('game_id'))
        self.assertEqual(2, len(result.get('players')))

        # check two players' id
        names = [player.get('name') for player in result.get('players')]
        # TODO figure out why it becomes Player(<id>,[]) form?
        self.assertEqual("['1', '2']", str(names))

    def test_get_status(self):
        repo = GameRepositoryInMemoryImpl()

        # given a started game with two players
        service = GameService(repo)
        game_id = service.create_game(Player.create("1").name)
        service.join_game(game_id, Player.create("2").name)
        result = service.start_game(game_id)
        self.assertTrue(result)

        # when get game status
        status_of_player1: GameStatus = GameStatus.parse_obj(service.get_status(game_id, '1'))
        status_of_player2: GameStatus = GameStatus.parse_obj(service.get_status(game_id, '2'))

        # then players should only know their own information
        def check_private_not_leaky(player_id, last_round):
            # check player list
            for p in last_round.players:
                if p.name == player_id:
                    # players can see their cards
                    self.assertTrue(len(p.cards) >= 1)
                else:
                    # player can not see others' cards
                    self.assertEqual(0, len(p.cards))

            # check turn player
            if last_round.turn_player.name == player_id:
                # players can see their cards
                self.assertTrue(len(last_round.turn_player.cards) >= 1)
            else:
                # player can not see others' cards
                self.assertEqual(0, len(last_round.turn_player.cards))

        check_private_not_leaky('1', status_of_player1.rounds[-1])
        check_private_not_leaky('2', status_of_player2.rounds[-1])
