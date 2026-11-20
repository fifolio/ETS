from app.types.credit_balance import CreditBalance


def test_the_total_adds_up_every_kind():
    assert CreditBalance(subscription=1, promotional=2, purchased=3).total == 6
