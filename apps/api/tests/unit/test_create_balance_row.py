import app.services.credits.create_balance_row as module


class FakeTables:
    def __init__(self):
        self.calls = []

    def create_row(self, **kwargs):
        self.calls.append(kwargs)


def test_the_row_id_is_the_user_id_and_only_the_granted_column_is_set(monkeypatch):
    tables = FakeTables()
    monkeypatch.setattr(module, "get_tables_db", lambda: tables)

    module.create_balance_row("user-1", "purchased", 25)

    assert tables.calls[0]["row_id"] == "user-1"
    assert tables.calls[0]["data"] == {"purchasedCredits": 25}
