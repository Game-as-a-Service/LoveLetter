from love_letter.models import Game, Player
from love_letter.models.cards import find_card_by_name

database = dict()


def build_fake_data():
    global database

    game = Game()
    game.id = 'g-5566'
    database['g-5566'] = game

    player_a = Player()
    player_a.name = 'player-a'
    player_a.cards = [find_card_by_name('衛兵'), find_card_by_name('公主')]
    game.add_player(player_a)

    player_b = Player()
    player_b.name = 'player-b'
    player_b.cards = [find_card_by_name('神父')]
    game.add_player(player_b)


build_fake_data()


class GameService:

    def start_game(self, game_id: str):
        if game_id not in database:
            return
        game: Game = database.get(game_id)
        game.next_round()
        return game.to_json()

    def play_card(self, game_id, card_action):
        if game_id in database:
            game: Game = database.get(game_id)
            game.play(card_action)
            return game.to_json()
        return None
