from typing import Dict, List
from unittest import TestCase

from love_letter.models import Game, Player
from love_letter.repository.data import GameData


class GameDataTest(TestCase):
    def setUp(self) -> None:
        self.game_id = "c-8763"
        self.game: Game = Game()
        self.game.id = self.game_id
        self.game.join(Player(name="1"))
        self.game.join(Player(name="2", user_id="2222"))
        self.game.start()

    def test_to_domain(self):
        game_dict = GameData.to_dict(self.game)
        game_domain = GameData.to_domain(game_dict)
        self.assertEqual(game_dict["game_id"], game_domain.id)
        self.assertEqual(game_dict["events"], game_domain.events)
        self.assertPlayers(game_dict["players"], game_domain.players)
        self.assertRounds(game_dict["rounds"], game_domain.rounds)

    def assertPlayers(self, players_dict: List[Dict], players_domain: List["Player"]):
        self.assertEqual(len(players_dict), len(players_domain))
        for index, player_dict in enumerate(players_dict):
            player_domain = players_domain[index]
            self.assertEqual(player_dict["name"], player_domain.name)
            self.assertEqual(player_dict["out"], player_domain.am_i_out)
            self.assertSeenCards(player_dict["seen_cards"], player_domain.seen_cards)
            self.assertCards(player_dict["cards"], player_domain.cards)
            self.assertEqual(player_dict["score"], player_domain.tokens_of_affection)
            self.assertEqual(player_dict["id"], player_domain.id)

    def assertSeenCards(
        self, seen_cards_dict: Dict, seen_cards_domain: List["SeenData"]
    ):
        self.assertEqual(len(seen_cards_dict), len(seen_cards_domain))
        for index, seen_card in enumerate(seen_cards_dict):
            seen_card_domain = seen_cards_domain[index]
            self.assertEqual(seen_card["opponent_name"], seen_card_domain.opponent_name)
            self.assertCards(seen_card["card"], seen_card_domain.card)

    def assertCards(self, cards_dict: Dict, cards_domain: List["Card"]):
        self.assertEqual(len(cards_dict), len(cards_domain))
        for index, card_dict in enumerate(cards_dict):
            card_domain = cards_domain[index]
            card_description = card_domain._card_data.get(
                str(card_domain.value), dict(name="<unknown>", description="<unknown>")
            )
            self.assertEqual(card_dict["name"], card_domain.name)
            self.assertEqual(card_dict["value"], card_domain.value)
            self.assertEqual(card_dict["description"], card_description["description"])

    def assertRounds(self, rounds_dict: Dict, rounds_domain: List["Round"]):
        self.assertEqual(len(rounds_dict), len(rounds_domain))
        for index, round_dict in enumerate(rounds_dict):
            round_domain = rounds_domain[index]
            self.assertPlayers(round_dict["players"], round_domain.players)
            self.assertEqual(round_dict["winner"], round_domain.winner)
            self.assertEqual(round_dict["start_player"], round_domain.start_player)
            self.assertPlayers([round_dict["turn_player"]], [round_domain.turn_player])
            self.assertDeck(round_dict["deck"], round_domain.deck)

    def assertDeck(self, deck_dict: Dict, deck_domain: "Deck"):
        self.assertCards(deck_dict["cards"], deck_domain.cards)
        self.assertCards(
            deck_dict["remove_by_rule_cards"], deck_domain.remove_by_rule_cards
        )
