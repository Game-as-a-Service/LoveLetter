from behave import given, when, then

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


@given('{player} 被侍女保護中')
def player_is_protected(context, player):
    p = Player()
    p.name = player
    p.protected = True
    setattr(context, player, p)


@when('系統發牌給 {player} {card1}')
def system_draw_card(context, player: str, card1: str):
    active_player: Player = getattr(context, player)
    draw_card = find_card_by_name(card1)
    active_player.cards.append(draw_card)


@when('{player_a} 對 {player_b} 出牌 {card1} 指定 {card2}')
def player_hold_one_card(context, player_a, player_b, card1, card2):
    active_player: Player = getattr(context, player_a)
    inactive_player: Player = getattr(context, player_b)

    active_player.play_opponent_two_cards(inactive_player,
                                          find_card_by_name(card1),
                                          find_card_by_name(card2)
                                          )


@when('{player_a} 對 {player_b} 出牌 {card}')
def player_hold_one_card(context, player_a, player_b, card):
    active_player: Player = getattr(context, player_a)
    inactive_player: Player = getattr(context, player_b)

    active_player.play_opponent_two_cards(opponent=inactive_player,
                                          card_will_be_played=find_card_by_name(card),
                                          )


@when('{player} 出牌 {card1}')
def player_play_card(context, player: str, card1: str):
    active_player: Player = getattr(context, player)
    card_will_be_played = find_card_by_name(card1)
    result = active_player.play_opponent_two_cards(opponent=active_player, card_will_be_played=card_will_be_played)


@then('{player} 出局')
def player_out(context, player):
    p: Player = getattr(context, player)
    assert p.am_i_out is True


@then('{player} 未出局')
def player_not_out(context, player):
    p: Player = getattr(context, player)
    assert p.am_i_out is False


@then('{player} 成功打出 {card}')
def player_success_play_this_card(context, player: str, card: str):
    active_player: Player = getattr(context, player)
    card_will_be_played = find_card_by_name(card)
    result = active_player.play_opponent_two_cards(card_will_be_played=card_will_be_played)

    assert result is True
    assert active_player.total_value_of_card == card_will_be_played.value


@then('{player} 丟棄手牌')
def player_discard_card(context, player: str):
    active_player: Player = getattr(context, player)
    assert len(active_player.cards) == 0


@then('{player} 無法打出 {card}')
def player_error_play_this_card(context, player: str, card: str):
    active_player: Player = getattr(context, player)
    card_will_be_played = find_card_by_name(card)
    result = active_player.play_opponent_two_cards(card_will_be_played=card_will_be_played)

    assert result is False
    assert active_player.total_value_of_card == 0

