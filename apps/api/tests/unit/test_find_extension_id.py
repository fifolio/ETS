from types import SimpleNamespace

import app.services.extensions.find_extension_id as module


class FakeTables:
    def __init__(self, rows):
        self.rows = rows

    def list_rows(self, **kwargs):
        return SimpleNamespace(rows=self.rows)


def test_returns_the_row_id_of_the_install(monkeypatch):
    monkeypatch.setattr(module, "get_tables_db", lambda: FakeTables([SimpleNamespace(id="row-1")]))

    assert module.find_extension_id("user-1", "install-12345678") == "row-1"


def test_returns_none_for_an_install_that_never_registered(monkeypatch):
    monkeypatch.setattr(module, "get_tables_db", lambda: FakeTables([]))

    assert module.find_extension_id("user-1", "install-12345678") is None
