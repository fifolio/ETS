from types import SimpleNamespace

import app.services.credits.list_credit_history as module


class FakeTables:
    def __init__(self, rows):
        self.rows = rows
        self.kwargs = None

    def list_rows(self, **kwargs):
        self.kwargs = kwargs
        return SimpleNamespace(rows=self.rows)


def row(amount, kind, reason, created="2026-12-01T10:00:00+00:00"):
    return SimpleNamespace(
        id="r", data=SimpleNamespace(amount=amount, kind=kind, reason=reason), created_at=created
    )


def test_maps_the_ledger_rows(monkeypatch):
    monkeypatch.setattr(
        module,
        "get_tables_db",
        lambda: FakeTables(
            [row(-1, "subscription", "Job scan"), row(25, "promotional", "Welcome bonus")]
        ),
    )

    entries = module.list_credit_history("user-1")

    assert [(e.amount, e.kind, e.reason) for e in entries] == [
        (-1, "subscription", "Job scan"),
        (25, "promotional", "Welcome bonus"),
    ]
    assert entries[0].created_at == "2026-12-01T10:00:00+00:00"


def test_asks_for_this_users_latest_rows_newest_first(monkeypatch):
    tables = FakeTables([])
    monkeypatch.setattr(module, "get_tables_db", lambda: tables)

    module.list_credit_history("user-1")

    joined = " ".join(tables.kwargs["queries"])
    assert "userId" in joined and "user-1" in joined and "$createdAt" in joined and "20" in joined


def test_no_rows_gives_an_empty_list(monkeypatch):
    monkeypatch.setattr(module, "get_tables_db", lambda: FakeTables([]))

    assert module.list_credit_history("user-1") == []
