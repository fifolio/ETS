import app.services.credits.read_user_credits as module
from app.types.credit_balance import CreditBalance


def install(monkeypatch, balance):
    order = []
    monkeypatch.setattr(
        module, "ensure_credit_account", lambda user_id, now: order.append("ensure")
    )

    def get_balance(user_id):
        order.append("read")
        return balance

    monkeypatch.setattr(module, "get_credit_balance", get_balance)
    return order


def test_creates_the_credit_account_first_and_returns_the_balances(monkeypatch):
    order = install(monkeypatch, CreditBalance(subscription=10, promotional=2, purchased=5))

    result = module.read_user_credits("user-1")

    assert order == ["ensure", "read"]
    assert (result.subscription, result.promotional, result.purchased) == (10, 2, 5)
    assert (result.total, result.credits_per_scan) == (17, 1)


def test_a_missing_balance_row_shows_zeros(monkeypatch):
    install(monkeypatch, None)

    assert module.read_user_credits("user-1").total == 0
