from typing import Dict, List

from love_letter.models import Card, Game, Player, Round, Seen


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
        )

    @staticmethod
    def to_domain(game_dict: Dict) -> "Game":
        game = Game()
        game.id = game_dict["game_id"]
        game.events = game_dict["events"]
        game.players = [PlayerData.to_domain(p) for p in game_dict["players"]]
        game.rounds = game_dict["rounds"]
        game.final_winner = game_dict["final_winner"]
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
        )

    @staticmethod
    def to_domain(player_dict: Dict) -> "Player":
        player = Player(player_dict["name"])
        player.am_i_out = player_dict["out"]
        player.cards = []
        player.seen_cards = []
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
        )

    @staticmethod
    def to_domain(round_dict: Dict) -> "Round":
        # player = Player(player_dict["name"])
        # player.am_i_out = player_dict["out"]
        # player.cards = []
        # player.seen_cards = []
        # player.tokens_of_affection = player_dict["score"]
        # return player
        pass


class SeenData:
    @staticmethod
    def to_dict(
        seen: Seen, hand_card: List[str], player: "Player", last_round: "Round"
    ) -> Dict:
        return dict(
            opponent_name=seen.opponent_name,
            card=CardData.to_dict(seen.card, hand_card, player, last_round),
        )

    @staticmethod
    def to_domain(round_dict: Dict) -> "Round":
        # player = Player(player_dict["name"])
        # player.am_i_out = player_dict["out"]
        # player.cards = []
        # player.seen_cards = []
        # player.tokens_of_affection = player_dict["score"]
        # return player
        pass


class CardData:
    @staticmethod
    def to_dict(
        card: "Card", hand_card: List[str], player: "Player", last_round: "Round"
    ) -> Dict:
        last_round_alive_players = [
            pl.name for pl in last_round.players if not pl.am_i_out
        ]
        data = card._card_data.get(
            str(card.value), dict(name="<unknown>", description="<unknown>")
        )
        return dict(
            name=card.name,
            description=data.get("description"),
            value=card.value,
            usage=card.usage(hand_card, player.name, last_round_alive_players),
        )

    @staticmethod
    def to_domain(round_dict: Dict) -> "Round":
        # player = Player(player_dict["name"])
        # player.am_i_out = player_dict["out"]
        # player.cards = []
        # player.seen_cards = []
        # player.tokens_of_affection = player_dict["score"]
        # return player
        pass
