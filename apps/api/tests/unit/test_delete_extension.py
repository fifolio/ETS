from types import SimpleNamespace

import app.services.extensions.delete_extension as module


class FakeTables:
    def __init__(self, rows):
        self.rows = rows
        self.queries = None
        self.deleted = []

    def list_rows(self, **kwargs):
        self.queries = kwargs["queries"]
        return SimpleNamespace(rows=self.rows)

    def delete_row(self, **kwargs):
        self.deleted.append(kwargs["row_id"])


def test_deletes_an_install_of_the_user(monkeypatch):
    tables = FakeTables([SimpleNamespace(id="ext-1")])
    monkeypatch.setattr(module, "get_tables_db", lambda: tables)

    assert module.delete_extension("user-1", "ext-1") is True
    assert tables.deleted == ["ext-1"]


def test_returns_false_and_deletes_nothing_for_an_unknown_or_foreign_install(monkeypatch):
    tables = FakeTables([])
    monkeypatch.setattr(module, "get_tables_db", lambda: tables)

    assert module.delete_extension("user-1", "ext-9") is False
    assert tables.deleted == []


def test_looks_the_install_up_by_id_and_by_owner(monkeypatch):
    tables = FakeTables([])
    monkeypatch.setattr(module, "get_tables_db", lambda: tables)

    module.delete_extension("user-1", "ext-1")

    joined = " ".join(tables.queries)
    assert "$id" in joined and "ext-1" in joined
    assert "userId" in joined and "user-1" in joined
