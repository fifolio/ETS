from app.constants.credits import WELCOME_CREDITS
from app.constants.plans import PLANS

EXPLORE, NEXT_MOVE, URGENT = PLANS


def test_explore_is_free_with_15_monthly_credits():
    assert (EXPLORE.price_usd_per_month, EXPLORE.subscription_credits) == (0.0, 15)


def test_next_move_costs_7_dollars_for_150_monthly_credits():
    assert (NEXT_MOVE.price_usd_per_month, NEXT_MOVE.subscription_credits) == (7.0, 150)


def test_urgent_costs_14_dollars_for_300_monthly_credits():
    assert (URGENT.price_usd_per_month, URGENT.subscription_credits) == (14.0, 300)


def test_the_welcome_bonus_is_one_amount_for_everyone():
    assert WELCOME_CREDITS == 25
    assert not hasattr(EXPLORE, "promotional_credits")
