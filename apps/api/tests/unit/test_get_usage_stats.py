from types import SimpleNamespace

import app.services.usage.get_usage_stats as module


class FakeTables:
    def __init__(self, rows):
        self.rows = rows

    def list_rows(self, **kwargs):
        return SimpleNamespace(rows=self.rows)


def test_reads_the_running_totals(monkeypatch):
    row = SimpleNamespace(
        data=SimpleNamespace(scanCount=12, wordsTotal=8400, minutesTotal=37.3333, cashTotal=31.1111)
    )
    monkeypatch.setattr(module, "get_tables_db", lambda: FakeTables([row]))

    stats = module.get_usage_stats("user-1")

    assert (stats.scans, stats.words, stats.minutes, stats.cash) == (12, 8400, 37.3333, 31.1111)


def test_a_user_who_never_scanned_has_zeros(monkeypatch):
    monkeypatch.setattr(module, "get_tables_db", lambda: FakeTables([]))

    stats = module.get_usage_stats("user-1")

    assert (stats.scans, stats.words, stats.minutes, stats.cash) == (0, 0, 0.0, 0.0)
