from types import SimpleNamespace

import app.services.payments.list_payment_history as module
from app.services.payments.build_payment_history_queries import build_payment_history_queries


class FakeTables:
    def __init__(self, rows, total):
        self.rows = rows
        self.total = total
        self.kwargs = None

    def list_rows(self, **kwargs):
        self.kwargs = kwargs
        return SimpleNamespace(rows=self.rows, total=self.total)


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


def test_maps_the_payments_and_the_page_information(monkeypatch):
    tables = FakeTables([row()], 11)
    monkeypatch.setattr(module, "get_tables_db", lambda: tables)

    page = module.list_payment_history("user-1", 1, "all", "all")

    entry = page.items[0]
    assert (entry.sku, entry.amount_cents, entry.credits, entry.status) == (
        "topup",
        500,
        40,
        "completed",
    )
    assert (page.total, page.total_pages) == (11, 2)
    assert tables.kwargs["queries"] == build_payment_history_queries("user-1", 1, "all", "all")


def test_the_applied_date_is_used_and_otherwise_the_creation_date(monkeypatch):
    rows = [row(), row(status="failed", applied=None)]
    monkeypatch.setattr(module, "get_tables_db", lambda: FakeTables(rows, 2))

    page = module.list_payment_history("user-1", 1, "all", "all")

    assert [e.paid_at for e in page.items] == [
        "2026-12-01T10:00:00+00:00",
        "2026-12-01T09:00:00+00:00",
    ]


def test_no_payments_gives_one_empty_page(monkeypatch):
    monkeypatch.setattr(module, "get_tables_db", lambda: FakeTables([], 0))

    page = module.list_payment_history("user-1", 1, "completed", "topup")

    assert (page.items, page.total, page.total_pages) == ([], 0, 1)
