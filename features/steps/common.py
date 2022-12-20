from behave import given, when, then

from love_letter.models import Player
from love_letter.models.cards import find_card_by_name, Deck


def as_player(context, player: str):
    if not hasattr(context, player):
        p = Player()
        p.name = player
        return p

    return getattr(context, player)


@given('{player} 持有 {card1} {card2}')
def player_hold_two_cards(context, player, card1, card2):
    p = as_player(context, player)
    p.cards = [find_card_by_name(card1), find_card_by_name(card2)]
    setattr(context, player, p)


@given('{player} 持有 {card}')
def player_hold_one_card(context, player, card):
    p = as_player(context, player)
    p.cards = [find_card_by_name(card)]
    setattr(context, player, p)


@given('{player} 被侍女保護中')
def player_is_protected(context, player):
    p = as_player(context, player)
    p.protected = True
    setattr(context, player, p)


@when('{player_a} 對 {player_b} 出牌 {card1} 指定 {card2}')
def player_hold_one_card(context, player_a, player_b, card1, card2):
    turn_player: Player = getattr(context, player_a)
    chosen_player: Player = getattr(context, player_b)

    turn_player.discard_card(chosen_player=chosen_player,
                             discarded_card=find_card_by_name(card1),
                             with_card=find_card_by_name(card2))


@when('{player_a} 對 {player_b} 出牌 {card}')
def player_hold_one_card(context, player_a, player_b, card):
    turn_player: Player = getattr(context, player_a)
    chosen_player: Player = getattr(context, player_b)

    turn_player.discard_card(chosen_player=chosen_player, discarded_card=find_card_by_name(card))


@when('{player} 出牌 {card1}')
def player_play_card(context, player: str, card1: str):
    turn_player: Player = getattr(context, player)
    discarded_card = find_card_by_name(card1)

    found_exception = False
    try:
        turn_player.discard_card(chosen_player=turn_player, discarded_card=discarded_card)
    except ValueError as e:
        found_exception = True
        assert e.args[0] == "You can not discard by the rule"

    setattr(context, "result", found_exception)


@then('{player} 出局')
def player_out(context, player):
    p: Player = getattr(context, player)
    assert p.am_i_out is True


@then('{player} 未出局')
def player_not_out(context, player):
    p: Player = getattr(context, player)
    assert p.am_i_out is False


@then('{player} 成功打出')
def player_success_play_this_card(context, player: str):
    result = getattr(context, "result")
    assert result is False


@then('{player} 無法打出')
def player_error_play_this_card(context, player: str):
    result = getattr(context, "result")
    assert result is True


@then('{player} 丟棄手牌 {card}')
def player_discard_card(context, player: str, card: str):
    turn_player: Player = getattr(context, player)
    card_result = find_card_by_name(card)
    turn_player.drop_card(card_result)
    assert len(turn_player.cards) == 0


@then('{player} 丟棄手牌')
def player_discard_card(context, player: str):
    turn_player: Player = getattr(context, player)
    assert len(turn_player.cards) == 0


@then('{player_a} 看到了 {player_b} 的 {card}')
def player_saw_opponent_hand(context, player_a, player_b, card):
    turn_player: Player = getattr(context, player_a)
    chosen_player: Player = getattr(context, player_b)
    card_will_be_checked = find_card_by_name(card)
    # check last seen_cards opponent name and card equal
    assert (turn_player.seen_cards[-1].opponent_name == chosen_player.name) is True
    assert (turn_player.seen_cards[-1].card == card_will_be_checked) is True


@then('{player_a} 擁有保護效果')
def player_get_protected(context, player_a):
    turn_player: Player = getattr(context, player_a)
    assert turn_player.protected is True


@then("{player} 剩一張手牌")
def player_left_one_card(context, player):
    turn_player: Player = getattr(context, player)
    assert len(turn_player.cards) == 1


@then("{player} 什麼也沒看到")
def player_saw_nothing(context, player):
    turn_player: Player = getattr(context, player)
    assert len(turn_player.seen_cards) == 0


@then('{player} 手牌為 {card}')
def player_error_play_this_card(context, player, card):
    turn_player: Player = getattr(context, player)
    card_result = find_card_by_name(card)
    assert (turn_player.cards[0] == card_result) is True


@then('{player_a} 對 {player_b} 出牌 {card1} 無法指定 {card2}')
def player_error_specify(context, player_a, player_b, card1, card2):
    turn_player: Player = getattr(context, player_a)
    chosen_player: Player = getattr(context, player_b)
    card_result_1 = find_card_by_name(card1)
    card_result_2 = find_card_by_name(card2)
    found_exception = False
    try:
        turn_player.discard_card(chosen_player=chosen_player,
                                 discarded_card=card_result_1,
                                 with_card=card_result_2)
    except ValueError as e:
        found_exception = True
    assert found_exception
