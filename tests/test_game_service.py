import unittest

from love_letter.models import Game, Player, Round, ToSomeoneCard
from love_letter.repository import create_default_repository
from love_letter.usecase.create_game import CreateGame
from love_letter.usecase.get_status import GetStatus
from love_letter.usecase.join_game import JoinGame
from love_letter.usecase.play_card import PlayCard
from love_letter.usecase.start_game import StartGame
from love_letter.web.dto import GameStatus
from love_letter.web.presenter import CreateGamePresenter, build_player_view
from tests.test_card_behave import reset_deck


def get_status(game_id: str, player_id: str):
    presenter = GetStatus.presenter()
    GetStatus().execute(GetStatus.input(game_id, player_id), presenter)
    game = presenter.as_view_model()
    result = build_player_view(game, player_id)
    return result


class GameServiceTests(unittest.TestCase):
    def test_create_and_join_game(self):
        # create a new game by usecase
        game_id = self.create_game()
        self.assertIsNotNone(game_id)

        # join the second player
        self.assertTrue(self.join_game(game_id))
        result = get_status(game_id, "1")

        self.assertIsNotNone(result)
        # # check the game status

        if result is None:
            raise ValueError("result is None.")

        self.assertEqual(game_id, result.get("game_id"))
        players = result.get("players")

        if players is None:
            raise ValueError("players is found in result.")

        self.assertEqual(2, len(players))

        # check two players' id
        names = [
            player.get("name") if not isinstance(player, str) else None
            for player in players
        ]
        # TODO figure out why it becomes Player(<id>,[]) form?
        self.assertEqual("['1', '2']", str(names))

    def join_game(self, game_id):
        presenter = JoinGame.presenter()
        JoinGame().execute(JoinGame.input(game_id, "2"), presenter)
        return presenter.as_view_model()

    def create_game(self):
        presenter = CreateGamePresenter.presenter()
        CreateGame().execute(CreateGame.input("1"), presenter)
        return presenter.as_view_model()

    def test_get_status(self):
        create_default_repository()

        # given a started game with two players
        # create a new game by usecase
        game_id = self.create_game()
        self.join_game(game_id)

        presenter = StartGame.presenter()
        StartGame().execute(StartGame.input(game_id), presenter)
        self.assertTrue(presenter.as_view_model())

        # when get game status
        status_of_player1: GameStatus = GameStatus.parse_obj(get_status(game_id, "1"))
        status_of_player2: GameStatus = GameStatus.parse_obj(get_status(game_id, "2"))

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

        check_private_not_leaky("1", status_of_player1.rounds[-1])
        check_private_not_leaky("2", status_of_player2.rounds[-1])


class PlayerContextTest(unittest.TestCase):
    def setUp(self) -> None:
        self.game_id = "c-8763"
        self.game: Game = Game()
        self.game.id = self.game_id
        self.game.join(Player("1"))
        self.game.join(Player("2"))
        self.game.join(Player("3"))
        repo = create_default_repository()
        repo.save_or_update(self.game)

        # disable random-picker for the first round
        # it always returns the first player
        self.origin_choose_one_randomly = Round.choose_one_randomly
        Round.choose_one_randomly = lambda players: players[0]

    def tearDown(self) -> None:
        Round.choose_one_randomly = self.origin_choose_one_randomly

    def check_player_card_usage(self, player_name, last_round, card_mapping):
        def check(name, current_player):
            if name == current_player.name:
                cards, usage = card_mapping[current_player.name]
                self.assertEqual(cards, [c.name for c in current_player.cards])
                self.assertEqual(usage, [c.usage for c in current_player.cards])

        # check player list
        for p in last_round.players:
            check(player_name, p)

        # check turn_player list
        turn_player = last_round.turn_player
        check(player_name, turn_player)

    def assert_player_status_prompt(self, expected_card_mapping):
        """
        驗證玩家狀態提示
        :return:
        """
        # when get game status
        status_of_player1: GameStatus = GameStatus.parse_obj(
            get_status(self.game_id, "1")
        )
        status_of_player2: GameStatus = GameStatus.parse_obj(
            get_status(self.game_id, "2")
        )
        status_of_player3: GameStatus = GameStatus.parse_obj(
            get_status(self.game_id, "3")
        )

        # then player get the expected cards
        self.check_player_card_usage(
            "1", status_of_player1.rounds[-1], expected_card_mapping
        )
        self.check_player_card_usage(
            "2", status_of_player2.rounds[-1], expected_card_mapping
        )
        self.check_player_card_usage(
            "3", status_of_player3.rounds[-1], expected_card_mapping
        )

    def test_prompt_player_only_discard_countess_because_has_prince(self):
        """
        玩家1持有 王子 伯爵夫人，提示只能打出 伯爵夫人
        玩家2持有 國王 伯爵夫人，提示只能打出 伯爵夫人
        :return:
        """
        # given the arranged deck
        reset_deck(["王子", "國王", "伯爵夫人", "伯爵夫人", "伯爵夫人", "伯爵夫人"])

        # given a started game
        self.start_game(self.game_id)

        expected_card_mapping = {
            "1": (
                ["王子", "伯爵夫人"],
                [
                    {"can_discard": False, "choose_players": [], "can_guess_cards": []},
                    {"can_discard": True, "choose_players": [], "can_guess_cards": []},
                ],
            ),
            "2": (
                ["國王"],
                [{"can_discard": False, "choose_players": [], "can_guess_cards": []}],
            ),
            "3": (
                ["伯爵夫人"],
                [{"can_discard": False, "choose_players": [], "can_guess_cards": []}],
            ),
        }

        # then assert the player status prompt
        self.assert_player_status_prompt(expected_card_mapping)

        # when player-1 discard countess
        PlayCard().execute(
            PlayCard.input(self.game_id, "1", "伯爵夫人", None), PlayCard.presenter()
        )

        expected_card_mapping = {
            "1": (
                ["王子"],
                [{"can_discard": False, "choose_players": [], "can_guess_cards": []}],
            ),
            "2": (
                ["國王", "伯爵夫人"],
                [
                    {"can_discard": False, "choose_players": [], "can_guess_cards": []},
                    {"can_discard": True, "choose_players": [], "can_guess_cards": []},
                ],
            ),
            "3": (
                ["伯爵夫人"],
                [{"can_discard": False, "choose_players": [], "can_guess_cards": []}],
            ),
        }

        # then assert the player status prompt
        self.assert_player_status_prompt(expected_card_mapping)

    def test_prompt_player_discard_king_and_priest(self):
        """
        玩家1持有 國王 神父，提示都能打出，且提供可指定的player清單(不含自己)
        :return:
        """
        # given the arranged deck
        reset_deck(["國王", "男爵", "王子", "神父", "衛兵"])

        # given a started game
        self.start_game(self.game_id)

        # then player get the expected cards
        expected_card_mapping = {
            "1": (
                ["國王", "神父"],
                [
                    {
                        "can_discard": True,
                        "choose_players": ["2", "3"],
                        "can_guess_cards": [],
                    },
                    {
                        "can_discard": True,
                        "choose_players": ["2", "3"],
                        "can_guess_cards": [],
                    },
                ],
            ),
            "2": (
                ["男爵"],
                [{"can_discard": False, "choose_players": [], "can_guess_cards": []}],
            ),
            "3": (
                ["王子"],
                [{"can_discard": False, "choose_players": [], "can_guess_cards": []}],
            ),
        }

        # then assert the player status prompt
        self.assert_player_status_prompt(expected_card_mapping)

    def test_prompt_player_discard_baron_and_prince(self):
        """
        玩家1持有 男爵 王子，提示都能打出，且提供可指定的player清單，男爵不含自己，王子包含自己
        :return:
        """
        # given the arranged deck
        reset_deck(["男爵", "國王", "神父", "王子", "衛兵"])

        # given a started game
        self.start_game(self.game_id)

        expected_card_mapping = {
            "1": (
                ["男爵", "王子"],
                [
                    {
                        "can_discard": True,
                        "choose_players": ["2", "3"],
                        "can_guess_cards": [],
                    },
                    {
                        "can_discard": True,
                        "choose_players": ["1", "2", "3"],
                        "can_guess_cards": [],
                    },
                ],
            ),
            "2": (
                ["國王"],
                [{"can_discard": False, "choose_players": [], "can_guess_cards": []}],
            ),
            "3": (
                ["神父"],
                [{"can_discard": False, "choose_players": [], "can_guess_cards": []}],
            ),
        }

        # then assert the player status prompt
        self.assert_player_status_prompt(expected_card_mapping)

    def test_prompt_player_discard_guard_and_prince(self):
        """
        玩家1持有 衛兵 王子，提示都能打出，且提供可指定的player清單，衛兵不含自己，王子包含自己
        :return:
        """
        # given the arranged deck
        reset_deck(["衛兵", "國王", "神父", "王子", "衛兵"])

        # given a started game
        self.start_game(self.game_id)

        expected_card_mapping = {
            "1": (
                ["衛兵", "王子"],
                [
                    {
                        "can_discard": True,
                        "choose_players": ["2", "3"],
                        "can_guess_cards": ["神父", "男爵", "侍女", "王子", "國王", "伯爵夫人", "公主"],
                    },
                    {
                        "can_discard": True,
                        "choose_players": ["1", "2", "3"],
                        "can_guess_cards": [],
                    },
                ],
            ),
            "2": (
                ["國王"],
                [{"can_discard": False, "choose_players": [], "can_guess_cards": []}],
            ),
            "3": (
                ["神父"],
                [{"can_discard": False, "choose_players": [], "can_guess_cards": []}],
            ),
        }

        # then assert the player status prompt
        self.assert_player_status_prompt(expected_card_mapping)

    def test_just_1_can_see_opponent_card_by_priest_card(self):
        """
        測試丟棄神父牌後，只有自己可以看到"對方的牌"，其他人看不到
        :return:
        """
        # given the arranged deck
        reset_deck(["神父", "神父", "男爵", "衛兵", "衛兵"])

        # given a started game
        self.start_game(self.game_id)

        # when: 1對3打出神父
        PlayCard().execute(
            PlayCard.input(self.game_id, "1", "神父", ToSomeoneCard(chosen_player=3)),
            PlayCard.presenter(),
        )

        status_of_player1: GameStatus = GameStatus.parse_obj(
            get_status(self.game_id, "1")
        )
        status_of_player2: GameStatus = GameStatus.parse_obj(
            get_status(self.game_id, "2")
        )
        status_of_player3: GameStatus = GameStatus.parse_obj(
            get_status(self.game_id, "3")
        )

        # then: 只有1才能看到對方的牌。2、3看不到
        self.assertTrue(len(status_of_player1.rounds[-1].players[0].seen_cards) == 1)
        self.assertTrue(len(status_of_player2.rounds[-1].players[0].seen_cards) == 0)
        self.assertTrue(len(status_of_player3.rounds[-1].players[0].seen_cards) == 0)
        self.assertTrue(
            len(status_of_player2.rounds[-1].turn_player.seen_cards) == 0
        )  # turn_player = 玩家2

    def start_game(self, game_id):
        presenter = StartGame.presenter()
        StartGame().execute(StartGame.input(game_id), presenter)
