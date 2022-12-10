import unittest

from love_letter.models import Player
from love_letter.repository import GameRepositoryInMemoryImpl
from love_letter.service import GameService


class GameServiceTests(unittest.TestCase):

    def test_create_and_join_game(self):
        service = GameService(GameRepositoryInMemoryImpl())

        # create a new game
        game_id = service.create_game(Player.create("1"))
        self.assertIsNotNone(game_id)

        # join the second player
        self.assertTrue(service.join_game(game_id, Player.create("2")))
        result = service.start_game(game_id)

        # check the game status
        self.assertEqual(game_id, result.get('game_id'))
        self.assertEqual(2, len(result.get('players')))

        # check two players' id
        names = [player.get('name') for player in result.get('players')]
        # TODO figure out why it becomes Player(<id>,[]) form?
        self.assertEqual("[Player(1,[]), Player(2,[])]", str(names))
