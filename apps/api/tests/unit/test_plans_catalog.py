from app.constants.plans import PLANS

EXPLORE, NEXT_MOVE, URGENT = PLANS


def fields(plan):
    return (
        plan.price_usd_per_month,
        plan.subscription_credits,
        plan.promotional_credits,
        plan.topup_price_usd,
    )


def test_explore_is_free_with_15_credits_and_a_3_dollar_top_up():
    assert fields(EXPLORE) == (0.0, 15, 0, 3.0)


def test_next_move_costs_7_dollars_with_150_credits_and_a_25_credit_bonus():
    assert fields(NEXT_MOVE) == (7.0, 150, 25, 2.0)


def test_urgent_costs_14_dollars_with_300_credits_and_a_50_credit_bonus():
    assert fields(URGENT) == (14.0, 300, 50, 1.0)


def test_every_top_up_is_25_credits_and_gets_cheaper_with_the_plan():
    assert all(plan.topup_credits == 25 for plan in PLANS)
    prices = [plan.topup_price_usd for plan in PLANS]
    assert prices == sorted(prices, reverse=True) and len(set(prices)) == 3
