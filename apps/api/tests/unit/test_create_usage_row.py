import app.services.usage.create_usage_row as module
from app.types.scan_savings import ScanSavings


class FakeTables:
    def __init__(self):
        self.calls = []

    def create_row(self, **kwargs):
        self.calls.append(kwargs)


def test_the_row_id_is_the_user_id_and_starts_with_the_first_scan(monkeypatch):
    tables = FakeTables()
    monkeypatch.setattr(module, "get_tables_db", lambda: tables)

    module.create_usage_row("user-1", 900, ScanSavings(minutes=4.0, cash=3.3333))

    assert tables.calls[0]["row_id"] == "user-1"
    assert tables.calls[0]["data"] == {
        "scanCount": 1,
        "wordsTotal": 900,
        "minutesTotal": 4.0,
        "cashTotal": 3.3333,
    }
