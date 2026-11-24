import app.services.subscriptions.update_subscription_row as module


class FakeTables:
    def __init__(self):
        self.calls = []

    def update_row(self, **kwargs):
        self.calls.append(kwargs)


def test_updates_the_row_whose_id_is_the_user_id(monkeypatch):
    tables = FakeTables()
    monkeypatch.setattr(module, "get_tables_db", lambda: tables)

    module.update_subscription_row("user-1", {"plan": "nextmove"})

    assert (tables.calls[0]["row_id"], tables.calls[0]["data"]) == ("user-1", {"plan": "nextmove"})
