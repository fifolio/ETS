from types import SimpleNamespace

import app.services.credits.list_credit_history as module
from app.services.credits.build_credit_history_queries import build_credit_history_queries


class FakeTables:
    def __init__(self, rows, total):
        self.rows = rows
        self.total = total
        self.kwargs = None

    def list_rows(self, **kwargs):
        self.kwargs = kwargs
        return SimpleNamespace(rows=self.rows, total=self.total)


def row(amount, kind, reason, created="2026-12-01T10:00:00+00:00"):
    return SimpleNamespace(
        id="r", data=SimpleNamespace(amount=amount, kind=kind, reason=reason), created_at=created
    )


def test_maps_the_rows_and_the_page_information(monkeypatch):
    rows = [row(-1, "subscription", "Job scan"), row(25, "promotional", "Welcome bonus")]
    monkeypatch.setattr(module, "get_tables_db", lambda: FakeTables(rows, 25))

    page = module.list_credit_history("user-1", 2, "all", "all")

    assert [(e.amount, e.kind, e.reason) for e in page.items] == [
        (-1, "subscription", "Job scan"),
        (25, "promotional", "Welcome bonus"),
    ]
    assert page.items[0].created_at == "2026-12-01T10:00:00+00:00"
    assert (page.page, page.page_size, page.total, page.total_pages) == (2, 10, 25, 3)


def test_asks_for_the_page_and_filters_that_were_chosen(monkeypatch):
    tables = FakeTables([], 0)
    monkeypatch.setattr(module, "get_tables_db", lambda: tables)

    module.list_credit_history("user-1", 3, "purchased", "used")

    assert tables.kwargs["queries"] == build_credit_history_queries(
        "user-1", 3, "purchased", "used"
    )


def test_no_rows_gives_one_empty_page(monkeypatch):
    monkeypatch.setattr(module, "get_tables_db", lambda: FakeTables([], 0))

    page = module.list_credit_history("user-1", 1, "all", "all")

    assert (page.items, page.total, page.total_pages) == ([], 0, 1)
