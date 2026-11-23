import pytest

from app.exceptions.checkout_refused_error import CheckoutRefusedError
from app.services.payments.build_checkout_order import build_checkout_order
from app.types.authenticated_user import AuthenticatedUser


def make_user(plan):
    return AuthenticatedUser("user-1", "Jane Doe", "jane@example.com", True, {}, [], plan)


def test_an_explore_user_can_buy_next_move_for_7_dollars():
    order = build_checkout_order(make_user("explore"), "nextmove")

    assert (order.sku, order.amount_cents, order.credits) == ("plan_nextmove", 700, 150)


def test_a_next_move_user_can_upgrade_to_urgent_for_14_dollars():
    order = build_checkout_order(make_user("nextmove"), "urgent")

    assert (order.sku, order.amount_cents, order.credits) == ("plan_urgent", 1400, 300)


@pytest.mark.parametrize(
    ("amount", "cents", "credits"),
    [(3.0, 300, 24), (5.0, 500, 40), (10.0, 1000, 80), (50.0, 5000, 400)],
)
def test_a_top_up_buys_8_credits_per_dollar(amount, cents, credits):
    order = build_checkout_order(make_user("explore"), "topup", amount)

    assert (order.sku, order.amount_cents, order.credits) == ("topup", cents, credits)


def test_a_top_up_costs_the_same_on_every_plan():
    orders = [
        build_checkout_order(make_user(plan), "topup", 5.0)
        for plan in ("explore", "nextmove", "urgent")
    ]

    assert {(order.amount_cents, order.credits) for order in orders} == {(500, 40)}


def test_a_top_up_below_the_minimum_is_refused():
    with pytest.raises(CheckoutRefusedError):
        build_checkout_order(make_user("explore"), "topup", 0.75)


def test_a_top_up_above_the_maximum_is_refused():
    with pytest.raises(CheckoutRefusedError):
        build_checkout_order(make_user("explore"), "topup", 50.25)


def test_a_top_up_without_an_amount_is_refused():
    with pytest.raises(CheckoutRefusedError):
        build_checkout_order(make_user("explore"), "topup")


def test_buying_the_current_plan_again_is_refused():
    with pytest.raises(CheckoutRefusedError) as error:
        build_checkout_order(make_user("nextmove"), "nextmove")

    assert "already" in error.value.message


def test_an_unknown_product_is_refused():
    with pytest.raises(CheckoutRefusedError):
        build_checkout_order(make_user("explore"), "platinum")
