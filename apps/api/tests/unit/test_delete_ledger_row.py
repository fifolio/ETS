import app.services.credits.delete_ledger_row as module


class FakeTables:
    def __init__(self):
        self.calls = []

    def delete_row(self, **kwargs):
        self.calls.append(kwargs)


def test_deletes_the_row_by_id(monkeypatch):
    tables = FakeTables()
    monkeypatch.setattr(module, "get_tables_db", lambda: tables)

    module.delete_ledger_row("ledger-1")

    assert tables.calls[0]["row_id"] == "ledger-1"
