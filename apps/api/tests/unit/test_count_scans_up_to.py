from types import SimpleNamespace

import app.services.feedback.count_scans_up_to as module


class FakeTables:
    def __init__(self, count):
        self.count = count
        self.calls = 0

    def list_rows(self, **kwargs):
        self.calls += 1
        return SimpleNamespace(rows=[object()] * self.count)


def test_counts_the_rows_returned(monkeypatch):
    monkeypatch.setattr(module, "get_tables_db", lambda: FakeTables(7))
    assert module.count_scans_up_to("user-1", 15) == 7


def test_counts_zero_when_there_are_no_scans(monkeypatch):
    monkeypatch.setattr(module, "get_tables_db", lambda: FakeTables(0))
    assert module.count_scans_up_to("user-1", 15) == 0


def test_a_limit_of_zero_makes_no_request(monkeypatch):
    tables = FakeTables(5)
    monkeypatch.setattr(module, "get_tables_db", lambda: tables)

    assert module.count_scans_up_to("user-1", 0) == 0
    assert tables.calls == 0
