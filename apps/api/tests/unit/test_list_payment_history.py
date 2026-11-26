from types import SimpleNamespace

import app.services.payments.list_payment_history as module


class FakeTables:
    def __init__(self, rows):
        self.rows = rows

    def list_rows(self, **kwargs):
        return SimpleNamespace(rows=self.rows)


def row(
    status="completed",
    applied="2026-12-01T10:00:00+00:00",
    created="2026-12-01T09:00:00+00:00",
    sku="topup",
    cents=500,
    credits=40,
):
    data = SimpleNamespace(
        sku=sku, amountCents=cents, credits=credits, status=status, appliedAt=applied
    )
    return SimpleNamespace(id="r", data=data, created_at=created)


def test_maps_a_payment(monkeypatch):
    monkeypatch.setattr(module, "get_tables_db", lambda: FakeTables([row()]))

    entry = module.list_payment_history("user-1")[0]

    assert (entry.sku, entry.amount_cents, entry.credits, entry.status) == (
        "topup",
        500,
        40,
        "completed",
    )


def test_abandoned_checkouts_are_left_out(monkeypatch):
    monkeypatch.setattr(
        module, "get_tables_db", lambda: FakeTables([row(status="pending"), row(status="failed")])
    )

    assert [e.status for e in module.list_payment_history("user-1")] == ["failed"]


def test_the_applied_date_is_used_and_otherwise_the_creation_date(monkeypatch):
    monkeypatch.setattr(
        module, "get_tables_db", lambda: FakeTables([row(), row(status="failed", applied=None)])
    )

    entries = module.list_payment_history("user-1")

    assert [e.paid_at for e in entries] == [
        "2026-12-01T10:00:00+00:00",
        "2026-12-01T09:00:00+00:00",
    ]


def test_only_the_latest_ten_are_returned(monkeypatch):
    monkeypatch.setattr(module, "get_tables_db", lambda: FakeTables([row() for _ in range(15)]))

    assert len(module.list_payment_history("user-1")) == 10
