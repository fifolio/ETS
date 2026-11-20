from types import SimpleNamespace

import app.services.credits.read_credit_balance as module
from app.types.credit_balance import CreditBalance


class FakeTables:
    def __init__(self, rows):
        self.rows = rows

    def list_rows(self, **kwargs):
        return SimpleNamespace(rows=self.rows)


def test_reads_the_three_balances(monkeypatch):
    data = SimpleNamespace(subscriptionCredits=5, promotionalCredits=2, purchasedCredits=9)
    monkeypatch.setattr(module, "get_tables_db", lambda: FakeTables([SimpleNamespace(data=data)]))

    assert module.get_credit_balance("user-1") == CreditBalance(
        subscription=5, promotional=2, purchased=9
    )


def test_a_user_without_a_balance_row_gives_none(monkeypatch):
    monkeypatch.setattr(module, "get_tables_db", lambda: FakeTables([]))

    assert module.get_credit_balance("user-1") is None
