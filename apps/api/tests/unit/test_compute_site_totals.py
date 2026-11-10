from types import SimpleNamespace

import app.services.stats.compute_site_totals as module


def usage_row(user_id, scans, minutes, cash):
    data = SimpleNamespace(scanCount=scans, wordsTotal=0, minutesTotal=minutes, cashTotal=cash)
    return SimpleNamespace(id=user_id, data=data)


def test_adds_up_every_row_of_the_usage_table(monkeypatch):
    rows = [usage_row("u1", 10, 45.0, 37.5), usage_row("u2", 5, 22.5, 18.75)]
    monkeypatch.setattr(module, "iter_table_rows", lambda table_id, model, queries=None: iter(rows))

    totals = module.compute_site_totals()

    assert (totals.total_users, totals.total_scans) == (2, 15)
    assert (totals.total_minutes_saved, totals.total_cash_saved_usd) == (67.5, 56.25)


def test_an_empty_table_gives_zeros(monkeypatch):
    monkeypatch.setattr(module, "iter_table_rows", lambda table_id, model, queries=None: iter([]))

    totals = module.compute_site_totals()

    assert (totals.total_users, totals.total_scans, totals.total_hours_saved) == (0, 0, 0.0)
