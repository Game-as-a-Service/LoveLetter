from behave import *

from love_letter.models import Player
from love_letter.models.cards import find_card_by_name


@given('{player} 持有 {card1} {card2}')
def player_hold_two_cards(context, player, card1, card2):
    p = Player()
    p.name = player
    p.cards = [find_card_by_name(card1), find_card_by_name(card2)]
    setattr(context, player, p)


@given('{player} 持有 {card}')
def player_hold_one_card(context, player, card):
    p = Player()
    p.name = player
    p.cards = [find_card_by_name(card)]
    setattr(context, player, p)


@when('{player_a} 對 {player_b} 出牌 {card1} 指定 {card2}')
def player_hold_one_card(context, player_a, player_b, card1, card2):
    active_player: Player = getattr(context, player_a)
    inactive_player: Player = getattr(context, player_b)

    active_player.play_opponent_two_cards(inactive_player,
                                          find_card_by_name(card1),
                                          find_card_by_name(card2)
                                          )


@then('{player} 出局')
def player_out(context, player):
    p: Player = getattr(context, player)
    assert p.am_i_out is True


@then('{player} 未出局')
def player_not_out(context, player):
    p: Player = getattr(context, player)
    assert p.am_i_out is False
