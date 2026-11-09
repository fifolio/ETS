import app.services.usage.increment_usage as module
from app.types.scan_savings import ScanSavings


class FakeTables:
    def __init__(self):
        self.calls = []

    def increment_row_column(self, **kwargs):
        self.calls.append(kwargs)


def test_adds_the_scan_words_minutes_and_cash_to_the_row_of_the_user(monkeypatch):
    tables = FakeTables()
    monkeypatch.setattr(module, "get_tables_db", lambda: tables)

    module.increment_usage("user-1", 900, ScanSavings(minutes=4.0, cash=3.3333))

    assert [(c["row_id"], c["column"], c["value"]) for c in tables.calls] == [
        ("user-1", "scanCount", 1),
        ("user-1", "wordsTotal", 900),
        ("user-1", "minutesTotal", 4.0),
        ("user-1", "cashTotal", 3.3333),
    ]


def test_skips_the_columns_whose_value_is_zero(monkeypatch):
    tables = FakeTables()
    monkeypatch.setattr(module, "get_tables_db", lambda: tables)

    module.increment_usage("user-1", 0, ScanSavings(minutes=0.0, cash=0.0))

    assert [c["column"] for c in tables.calls] == ["scanCount"]
