from types import SimpleNamespace

import app.services.catalog.get_job_rate as module


class FakeTables:
    def __init__(self, rows):
        self.rows = rows

    def list_rows(self, **kwargs):
        return SimpleNamespace(rows=self.rows)


def test_returns_the_rate_of_the_job(monkeypatch):
    row = SimpleNamespace(data=SimpleNamespace(hourlyRateUsd=45.5))
    monkeypatch.setattr(module, "get_tables_db", lambda: FakeTables([row]))

    assert module.get_job_rate("job-1") == 45.5


def test_returns_none_for_an_unknown_job(monkeypatch):
    monkeypatch.setattr(module, "get_tables_db", lambda: FakeTables([]))

    assert module.get_job_rate("nope") is None
