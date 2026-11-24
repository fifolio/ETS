from types import SimpleNamespace

import app.services.payments.find_payment_row as module


class FakeTables:
    def __init__(self, rows):
        self.rows = rows
        self.queries = None

    def list_rows(self, **kwargs):
        self.queries = kwargs["queries"]
        return SimpleNamespace(rows=self.rows)


def row(**overrides):
    data = {
        "userId": "user-1",
        "sku": "topup",
        "providerCheckoutId": "ch_1",
        "providerPaymentId": None,
        "amountCents": 500,
        "credits": 40,
        "status": "pending",
        "appliedAt": None,
    }
    return SimpleNamespace(id="row-1", data=SimpleNamespace(**{**data, **overrides}))


def test_maps_the_row_and_asks_for_the_column_and_value(monkeypatch):
    tables = FakeTables([row()])
    monkeypatch.setattr(module, "get_tables_db", lambda: tables)

    record = module.find_payment_row("providerCheckoutId", "ch_1")

    assert (record.row_id, record.user_id, record.amount_cents, record.credits) == (
        "row-1",
        "user-1",
        500,
        40,
    )
    assert record.payment_id is None and record.applied is False
    joined = " ".join(tables.queries)
    assert "providerCheckoutId" in joined and "ch_1" in joined


def test_a_row_with_a_payment_and_an_applied_date_is_applied(monkeypatch):
    applied = row(providerPaymentId="pay_1", appliedAt="2026-12-01T10:00:00+00:00")
    monkeypatch.setattr(module, "get_tables_db", lambda: FakeTables([applied]))

    record = module.find_payment_row("providerPaymentId", "pay_1")

    assert record.payment_id == "pay_1" and record.applied is True


def test_no_row_gives_none(monkeypatch):
    monkeypatch.setattr(module, "get_tables_db", lambda: FakeTables([]))

    assert module.find_payment_row("providerPaymentId", "pay_9") is None
