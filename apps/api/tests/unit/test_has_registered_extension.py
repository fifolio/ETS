from types import SimpleNamespace

import app.services.extensions.has_registered_extension as module


class FakeTables:
    def __init__(self, rows):
        self.rows = rows

    def list_rows(self, **kwargs):
        return SimpleNamespace(rows=self.rows)


def test_true_when_the_user_has_at_least_one_install(monkeypatch):
    monkeypatch.setattr(module, "get_tables_db", lambda: FakeTables([object()]))

    assert module.has_registered_extension("user-1") is True


def test_false_when_the_user_has_none(monkeypatch):
    monkeypatch.setattr(module, "get_tables_db", lambda: FakeTables([]))

    assert module.has_registered_extension("user-1") is False
