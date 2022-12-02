from behave import given, when, then

from love_letter.models import Player
from love_letter.models.cards import find_card_by_name, Deck


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
    turn_player: Player = getattr(context, player)
    draw_card = find_card_by_name(card1)
    turn_player.cards.append(draw_card)


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
    turn_player.discard_card(chosen_player=turn_player, discarded_card=discarded_card)


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
    turn_player: Player = getattr(context, player)
    discarded_card = find_card_by_name(card)
    result = turn_player.discard_card(discarded_card=discarded_card)

    assert result is True
    assert turn_player.total_value_of_card == discarded_card.value


@then('{player} 丟棄手牌')
def player_discard_card(context, player: str):
    turn_player: Player = getattr(context, player)
    turn_player.drop_cards()
    assert len(turn_player.cards) == 0


@then('{player} 無法打出 {card}')
def player_error_play_this_card(context, player: str, card: str):
    turn_player: Player = getattr(context, player)
    discarded_card = find_card_by_name(card)

    found_exception = False
    try:
        i_dont_care_who_is_the_player = Player()
        turn_player.discard_card(chosen_player=i_dont_care_who_is_the_player,
                                 discarded_card=discarded_card,
                                 with_card=None)
    except ValueError as e:
        found_exception = True
        assert e.args[0] == "You can not discard by the rule"

    assert found_exception
    assert turn_player.total_value_of_card == 0


@then('{player_a} 看到了 {player_b} 的 {card}')
def player_saw_opponent_hand(context, player_a, player_b, card):
    turn_player: Player = getattr(context, player_a)
    chosen_player: Player = getattr(context, player_b)
    card_will_be_checked = find_card_by_name(card)
    # check last seen_cards opponent name and card equal
    assert (turn_player.seen_cards[-1].opponent_name == chosen_player.name) is True
    assert (turn_player.seen_cards[-1].card == card_will_be_checked) is True


@then('{player} 從牌庫拿一張牌')
def player_draw_card(context, player: str):
    turn_player: Player = getattr(context, player)
    deck = Deck()
    deck.shuffle(4)
    deck.draw(turn_player)
    assert len(turn_player.cards) == 1
