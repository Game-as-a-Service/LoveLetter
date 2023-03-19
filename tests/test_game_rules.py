from collections import Counter
from typing import Callable, List
from unittest import TestCase

from love_letter.models import Deck, Game, GuessCard, Player, Round


class _TestDeckForGameRules(Deck):
    def __init__(self, card_name_list):
        self.card_name_list = card_name_list

    def shuffle(self, player_num: int):
        super().shuffle(player_num)
        from love_letter.models import find_card_by_name as c

        self.cards = [c(x) for x in self.card_name_list]


def reset_deck(card_name_list: List[str]):
    import love_letter.models

    love_letter.models.deck_factory = lambda: _TestDeckForGameRules(card_name_list)


class CatchableTestCase(TestCase):
    def setUp(self):
        self.exception_message: str = ""

    def catch(self, callable: Callable):
        with self.assertRaises(BaseException) as ex:
            callable()
        self.exception_message = str(ex.exception)


class GetGameStartedTests(CatchableTestCase):
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
        game.join(Player("1"))
        game.join(Player("2"))

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
        game.join(Player("1"))
        game.join(Player("2"))
        game.start()

        # when a player join the started game
        self.catch(lambda: game.join(Player("3")))

        # then it got error
        self.assertEqual("Game Has Started", self.exception_message)

    def test_players_cannot_join_game_after_4th_player(self):
        """
        遊戲最多 4 個玩家，晚來的就不能加了。
        """

        # given a not started game with 4 players
        game: Game = Game()
        game.join(Player("1"))
        game.join(Player("2"))
        game.join(Player("3"))
        game.join(Player("4"))

        # when another player join the game
        self.catch(lambda: game.join(Player("5")))

        # then it got error
        self.assertEqual("Game Has No Capacity For New Players", self.exception_message)


class PlayingGameRoundByRoundTests(TestCase):
    def setUp(self):
        # make a game with 3 players
        game: Game = Game()
        game.join(Player("1"))
        game.join(Player("2"))
        game.join(Player("3"))
        self.game: Game = game

        # disable random-picker for the first round
        # it always returns the first player
        self.origin_choose_one_randomly = Round.choose_one_randomly
        Round.choose_one_randomly = lambda players: players[0]

    def tearDown(self) -> None:
        Round.choose_one_randomly = self.origin_choose_one_randomly

    def test_after_game_start_every_player_get_1_card_and_turn_player_get_extra_1(self):
        """
        遊戲開始後，人人獲得一張手牌。
        turn player 會再多一張手牌
        """

        # given the arranged deck
        reset_deck(
            [
                "王子",  # player 1
                "神父",  # player 2
                "公主",  # player 3
                "衛兵",  # turn player owns it
                "衛兵",
                "衛兵",
                "衛兵",
            ]
        )

        # when start the arranged game
        self.game.start()

        # then player get the expected cards
        expected_card_mapping = [("1", ["王子", "衛兵"]), ("2", ["神父"]), ("3", ["公主"])]
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
        reset_deck(list(["衛兵" for x in range(100)]))

        # given a started game
        self.game.start()

        # when 3 players discarded twice but nothing happened
        self.game.play("1", "衛兵", GuessCard(chosen_player="2", guess_card="公主"))
        self.game.play("2", "衛兵", GuessCard(chosen_player="3", guess_card="公主"))
        self.game.play("3", "衛兵", GuessCard(chosen_player="1", guess_card="公主"))
        self.game.play("1", "衛兵", GuessCard(chosen_player="2", guess_card="公主"))
        self.game.play("2", "衛兵", GuessCard(chosen_player="3", guess_card="公主"))
        self.game.play("3", "衛兵", GuessCard(chosen_player="1", guess_card="公主"))

        # then the game is still at round 1
        self.assertEqual(1, len(self.game.rounds))

        # then the turn player back to the player 1
        self.assertEqual("1", self.game.get_turn_player().name)

        # then the turn player earns 2 points by discarding 衛兵 twice
        self.assertEqual(2, self.game.get_turn_player().total_value_of_card)

    def test_move_to_next_round_by_only_one_player_alive(self):
        """
        當只剩下 1 名玩家存活時，此玩家為 winner，讓此局結束開始新的一局
        """

        # given the arranged deck
        reset_deck(["伯爵夫人", "國王", "王子"] + list(["衛兵" for x in range(10)]))

        # given a started game
        self.game.start()

        # when the game has only 1 player alive
        self.game.play(
            "1",
            "衛兵",  # player-1 kill player-2
            GuessCard(chosen_player="2", guess_card="國王"),
        )
        self.game.play(
            "3",
            "衛兵",  # player-3 kill player-1
            GuessCard(chosen_player="1", guess_card="伯爵夫人"),
        )

        # then the player-3 will be
        #   1. the winner of the last round
        #   2. the turn player at the new round
        self.assertEqual(2, len(self.game.rounds))  # there are two rounds
        self.assertEqual("3", self.game.rounds[-2].winner)  # the last round winner
        self.assertEqual(
            "3", self.game.get_turn_player().name
        )  # turn player of this round

    def test_move_to_next_round_by_empty_deck(self):
        """
        當牌庫已空時，決定最後的 winner。讓此局結束開始新的一局
        """

        # given the arranged deck
        reset_deck(["伯爵夫人", "公主", "國王", "衛兵"])

        # given a started game
        self.game.start()

        # when the deck become empty
        self.game.play(
            "1",
            "衛兵",  # player-1 kill nobody
            GuessCard(chosen_player="2", guess_card="侍女"),
        )

        # then player-2 is winner because 公主 is the card of the highest value (8)
        #   1. the winner of the last round
        #   2. the turn player at the new round
        self.assertEqual(2, len(self.game.rounds))  # there are two rounds
        self.assertEqual("2", self.game.rounds[-2].winner)  # the last round winner
        self.assertEqual(
            "2", self.game.get_turn_player().name
        )  # turn player of this round


class FirstRoundRandomPickerTests(TestCase):
    def create_game(self):
        # make a game with 4 players
        game: Game = Game()
        game.join(Player("1"))
        game.join(Player("2"))
        game.join(Player("3"))
        game.join(Player("4"))
        return game

    def test_uniform_random_picker(self):
        counter = Counter()
        for _ in range(100):
            game = self.create_game()
            game.start()
            counter.update({game.get_turn_player().name: 1})

        # any player has the chance to be the turn player
        for value in counter.values():
            self.assertTrue(value > 1)


class TurnPlayerCannotDiscardCardNotInTheirHandTests(CatchableTestCase):
    def setUp(self):
        # make a game with 2 players
        game: Game = Game()
        game.join(Player("1"))
        game.join(Player("2"))
        self.game: Game = game

    def test_turn_player_cannot_discard_cards_not_in_their_hand(self):
        # given the arranged deck
        reset_deck(["神父", "神父", "衛兵", "衛兵"])

        # given a started game
        self.game.start()

        # when player discard the card not in their hands
        turn_player = self.game.get_turn_player().name
        self.catch(lambda: self.game.play(turn_player, "公主", None))

        # then got error
        self.assertEqual(
            "Cannot discard cards not in your hand", self.exception_message
        )
