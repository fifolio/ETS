import pytest

from app.services.credits.plan_spend import plan_spend
from app.types.credit_balance import CreditBalance


@pytest.mark.parametrize(
    ("promotional", "subscription", "purchased", "amount", "expected"),
    [
        (2, 5, 7, 1, [("promotional", 1)]),
        (0, 5, 7, 1, [("subscription", 1)]),
        (0, 0, 7, 1, [("purchased", 1)]),
        (1, 5, 7, 3, [("promotional", 1), ("subscription", 2)]),
        (1, 1, 3, 4, [("promotional", 1), ("subscription", 1), ("purchased", 2)]),
        (1, 1, 1, 4, None),
        (0, 0, 0, 1, None),
        (5, 5, 5, 0, []),
    ],
)
def test_credits_are_used_promotional_then_subscription_then_purchased(
    promotional, subscription, purchased, amount, expected
):
    balance = CreditBalance(subscription=subscription, promotional=promotional, purchased=purchased)

    assert plan_spend(balance, amount) == expected
