import app.services.usage.increment_usage as module


class FakeTables:
    def __init__(self):
        self.calls = []

    def increment_row_column(self, **kwargs):
        self.calls.append(kwargs)


def test_adds_one_scan_and_the_words_to_the_row_of_the_user(monkeypatch):
    tables = FakeTables()
    monkeypatch.setattr(module, "get_tables_db", lambda: tables)

    module.increment_usage("user-1", 900)

    assert [(c["row_id"], c["column"], c["value"]) for c in tables.calls] == [
        ("user-1", "scanCount", 1),
        ("user-1", "wordsTotal", 900),
    ]


def test_skips_the_words_column_when_there_are_no_words(monkeypatch):
    tables = FakeTables()
    monkeypatch.setattr(module, "get_tables_db", lambda: tables)

    module.increment_usage("user-1", 0)

    assert [c["column"] for c in tables.calls] == ["scanCount"]
