from types import SimpleNamespace

import app.services.suggestions.count_pending_suggestions as module


class FakeTables:
    def __init__(self, rows):
        self.rows = rows
        self.queries = None

    def list_rows(self, **kwargs):
        self.queries = kwargs["queries"]
        return SimpleNamespace(rows=self.rows)


def test_counts_the_rows_returned(monkeypatch):
    monkeypatch.setattr(module, "get_tables_db", lambda: FakeTables([object()] * 4))

    assert module.count_pending_suggestions("user-1", 10) == 4


def test_asks_only_for_pending_suggestions_of_this_user(monkeypatch):
    tables = FakeTables([])
    monkeypatch.setattr(module, "get_tables_db", lambda: tables)

    module.count_pending_suggestions("user-1", 10)

    joined = " ".join(tables.queries)
    assert "userId" in joined and "user-1" in joined
    assert "status" in joined and "pending" in joined
