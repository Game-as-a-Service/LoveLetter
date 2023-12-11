from typing import Dict, List, Optional

from love_letter.models import Card, Deck, Game, Player, Round, Seen
from love_letter.models.cards import find_card_by_name


class GameData:
    @staticmethod
    def to_dict(game: "Game") -> Dict:
        last_round = game.rounds[-1] if len(game.rounds) > 0 else []
        return dict(
            game_id=game.id,
            events=game.events,
            players=[PlayerData.to_dict(x, last_round) for x in game.players],
            rounds=[RoundData.to_dict(x, last_round) for x in game.rounds],
            final_winner=game.final_winner,
            num_of_tokens_to_win=game.num_of_tokens_to_win,
        )

    @staticmethod
    def to_domain(game_dict: Dict) -> "Game":
        game = Game()
        game.id = game_dict["game_id"]
        game.events = game_dict["events"]
        game.players = [PlayerData.to_domain(p) for p in game_dict["players"]]
        game.rounds = [RoundData.to_domain(r) for r in game_dict["rounds"]]
        game.final_winner = game_dict["final_winner"]
        game.num_of_tokens_to_win = game_dict["num_of_tokens_to_win"]
        return game


class PlayerData:
    @staticmethod
    def to_dict(player: "Player", last_round: "Round") -> Dict:
        hand_cards = [c.name for c in player.cards]
        return dict(
            name=player.name,
            out=player.am_i_out,
            seen_cards=[
                SeenData.to_dict(x, hand_cards, player, last_round)
                for x in player.seen_cards
            ],
            cards=[
                CardData.to_dict(x, hand_cards, player, last_round)
                for x in player.cards
            ],
            score=player.tokens_of_affection,
            id=player.id,
        )

    @staticmethod
    def to_domain(player_dict: Dict) -> "Player":
        player = Player(player_dict["name"], player_dict["id"])
        player.am_i_out = player_dict["out"]
        player.cards = [CardData.to_domain(c) for c in player_dict["cards"]]
        player.seen_cards = [SeenData.to_domain(s) for s in player_dict["seen_cards"]]
        player.tokens_of_affection = player_dict["score"]
        return player


class RoundData:
    @staticmethod
    def to_dict(round: "Round", last_round: "Round") -> Dict:
        turn_player = (
            PlayerData.to_dict(round.turn_player, last_round)
            if round.turn_player is not None
            else {}
        )
        return dict(
            players=[PlayerData.to_dict(x, last_round) for x in round.players],
            winner=round.winner,
            turn_player=turn_player,
            start_player=round.start_player,
            deck=DeckData.to_dict(round.deck),
        )

    @staticmethod
    def to_domain(round_dict: Dict) -> "Round":
        deck = DeckData.to_domain(round_dict["deck"])
        turn_player = None
        players = []
        for player in round_dict["players"]:
            _player = PlayerData.to_domain(player)
            players.append(_player)
            if player["name"] == round_dict["turn_player"]["name"]:
                turn_player = _player
        _round = Round(players, deck)
        _round.winner = round_dict["winner"]
        _round.turn_player = turn_player
        _round.start_player = round_dict["start_player"]
        return _round


class DeckData:
    @staticmethod
    def to_dict(deck: "Deck") -> Dict:
        return dict(
            cards=[CardData.to_dict(c) for c in deck.cards],
            remove_by_rule_cards=[
                CardData.to_dict(c) for c in deck.remove_by_rule_cards
            ],
        )

    @staticmethod
    def to_domain(deck_dict: Dict) -> "Deck":
        deck = Deck()
        deck.cards = [CardData.to_domain(c) for c in deck_dict["cards"]]
        deck.remove_by_rule_cards = [
            CardData.to_domain(c) for c in deck_dict["remove_by_rule_cards"]
        ]
        return deck


class SeenData:
    @staticmethod
    def to_dict(
        seen: "Seen", hand_card: List[str], player: "Player", last_round: "Round"
    ) -> Dict:
        return dict(
            opponent_name=seen.opponent_name,
            card=CardData.to_dict(seen.card, hand_card, player, last_round),
        )

    @staticmethod
    def to_domain(seen_dict: Dict) -> "Seen":
        opponent_name = ""
        card = None
        if seen_dict.get("opponent_name"):
            opponent_name = seen_dict["opponent_name"]

        if seen_dict.get("card"):
            card = CardData.to_domain(seen_dict["card"])

        return Seen(opponent_name=opponent_name, card=card)


class CardData:
    @staticmethod
    def to_dict(
        card: "Card",
        hand_card: Optional[List[str]] = None,
        player: Optional["Player"] = None,
        last_round: Optional["Round"] = None,
    ) -> Dict:
        data = card._card_data.get(
            str(card.value), dict(name="<unknown>", description="<unknown>")
        )
        if hand_card is None or player is None or last_round is None:
            return dict(
                name=card.name, description=data.get("description"), value=card.value
            )

        last_round_alive_players = [
            p.name for p in last_round.players if not p.am_i_out
        ]
        return dict(
            name=card.name,
            description=data.get("description"),
            value=card.value,
            usage=card.usage(hand_card, player.name, last_round_alive_players),
        )

    @staticmethod
    def to_domain(card_dict: Dict) -> "Card":
        return find_card_by_name(card_dict["name"])
