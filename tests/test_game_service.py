import json
import unittest

from love_letter.models import Player, Game, Round
from love_letter.repository import GameRepositoryInMemoryImpl
from love_letter.service import GameService
from love_letter.web.dto import GameStatus
from tests.test_card_behave import reset_deck


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


class PlayerContextTest(unittest.TestCase):
    def setUp(self) -> None:
        self.game_id = "c-8763"
        self.game: Game = Game()
        self.game.id = self.game_id
        self.game.join(Player.create('1'))
        self.game.join(Player.create('2'))
        repo = GameRepositoryInMemoryImpl()
        repo.in_memory_data[self.game_id] = self.game
        self.game_service: GameService = GameService(repo)

        # disable random-picker for the first round
        # it always returns the first player
        self.origin_choose_one_randomly = Round.choose_one_randomly
        Round.choose_one_randomly = lambda x: x[0]

    def tearDown(self) -> None:
        Round.choose_one_randomly = self.origin_choose_one_randomly

    def check_player_card_usage(self, last_round, card_mapping):
        # check player list
        for p in last_round.players:
            cards, can_discard = card_mapping.get(p.name)
            self.assertEqual(cards, [x.name for x in p.cards])
            self.assertEqual(can_discard, [x.can_discard for x in p.cards])

        # check turn_player list
        turn_player = last_round.turn_player
        cards, can_discard = card_mapping.get(turn_player.name)
        self.assertEqual(cards, [x.name for x in turn_player.cards])
        self.assertEqual(can_discard, [x.can_discard for x in turn_player.cards])

    def test_prompt_player_only_discard_countess_because_has_prince(self):
        """
        玩家1持有 王子 伯爵夫人，提示只能打出 伯爵夫人
        玩家2持有 國王 伯爵夫人，提示只能打出 伯爵夫人
        :return:
        """
        # given the arranged deck
        reset_deck(['王子', '國王', '伯爵夫人', '伯爵夫人', '伯爵夫人'])

        # given a started game
        self.game_service.start_game(self.game_id)

        # when get game status
        status_of_player1: GameStatus = GameStatus.parse_obj(self.game_service.get_status(self.game_id, '1'))
        status_of_player2: GameStatus = GameStatus.parse_obj(self.game_service.get_status(self.game_id, '2'))

        # then player get the    expected cards
        expected_card_mapping1 = {'1': (['王子', '伯爵夫人'], [False, True]),
                                  '2': ([], [])}
        expected_card_mapping2 = {'1': ([], []),
                                  '2': (['國王'], [True])}

        self.check_player_card_usage(status_of_player1.rounds[-1], expected_card_mapping1)
        self.check_player_card_usage(status_of_player2.rounds[-1], expected_card_mapping2)

        # when player-1 play 伯爵夫人
        self.game_service.play_card(self.game_id, "1", '伯爵夫人', None)

        # when get game status
        status_of_player1: GameStatus = GameStatus.parse_obj(self.game_service.get_status(self.game_id, '1'))
        status_of_player2: GameStatus = GameStatus.parse_obj(self.game_service.get_status(self.game_id, '2'))

        # then player get the expected cards
        expected_card_mapping1 = {'1': (['王子'], [True]),
                                  '2': ([], [])}
        expected_card_mapping2 = {'1': ([], []),
                                  '2': (['國王', '伯爵夫人'], [False, True])}

        self.check_player_card_usage(status_of_player1.rounds[-1], expected_card_mapping1)
        self.check_player_card_usage(status_of_player2.rounds[-1], expected_card_mapping2)
