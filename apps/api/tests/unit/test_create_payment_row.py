import app.services.payments.create_payment_row as module


class FakeTables:
    def __init__(self):
        self.calls = []

    def create_row(self, **kwargs):
        self.calls.append(kwargs)


def test_stores_the_row_in_the_payments_table(monkeypatch):
    tables = FakeTables()
    monkeypatch.setattr(module, "get_tables_db", lambda: tables)
    data = {"userId": "user-1", "status": "pending"}

    module.create_payment_row(data)

    assert tables.calls[0]["data"] == data
    assert tables.calls[0]["row_id"]
