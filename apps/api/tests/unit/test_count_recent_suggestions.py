from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

import app.services.suggestions.count_recent_suggestions as module

NOW = datetime(2026, 11, 13, 12, 0, tzinfo=UTC)


class FakeTables:
    def __init__(self, rows):
        self.rows = rows
        self.queries = None

    def list_rows(self, **kwargs):
        self.queries = kwargs["queries"]
        return SimpleNamespace(rows=self.rows)


def test_counts_the_rows_returned(monkeypatch):
    monkeypatch.setattr(module, "get_tables_db", lambda: FakeTables([object(), object()]))

    assert module.count_recent_suggestions("user-1", NOW, 3) == 2


def test_no_rows_means_zero(monkeypatch):
    monkeypatch.setattr(module, "get_tables_db", lambda: FakeTables([]))

    assert module.count_recent_suggestions("user-1", NOW, 3) == 0


def test_asks_only_for_this_users_suggestions_of_the_last_24_hours(monkeypatch):
    tables = FakeTables([])
    monkeypatch.setattr(module, "get_tables_db", lambda: tables)

    module.count_recent_suggestions("user-1", NOW, 3)

    joined = " ".join(tables.queries)
    assert "userId" in joined and "user-1" in joined
    assert "$createdAt" in joined
    assert (NOW - timedelta(hours=24)).isoformat() in joined
