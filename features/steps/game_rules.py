from behave import given, then, when

from love_letter.models import Game, Player


@given('{player} 建立遊戲')
def player_create_a_game(context, player):
    p = Player()
    p.name = player
    game = Game.create(p)
    context.game = game
    context.exception = None


@when('{player} 開始遊戲')
def player_start_the_game(context, player):
    assert context.game is not None
    game: Game = context.game
    try:
        game.start()
    except Exception as e:
        # keep the exception for "then" step
        context.exception = e


@then('遊戲無法開始，因為 {reason}')
def game_cannot_get_started_because(context, reason: str):
    assert context.exception is not None
    assert reason == str(context.exception)
    context.exception = None


@given('{player} 加入遊戲')
def player_join_a_game(context, player):
    game: Game = context.game
    p = Player()
    p.name = player
    game.join(p)


@then('遊戲已經開始')
def game_cannot_get_started_because(context):
    game: Game = context.game
    assert game.has_started()


@then('{player} 無法加入遊戲，因為 {reason}')
def game_cannot_get_started_because(context, player, reason):
    game: Game = context.game
    p = Player()
    p.name = player

    exception = None
    try:
        game.join(p)
    except ValueError as e:
        exception = e

    assert exception is not None
    assert str(exception) == reason
