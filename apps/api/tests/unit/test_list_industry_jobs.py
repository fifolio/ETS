from types import SimpleNamespace

import app.services.catalog.list_industry_jobs as module


def row(row_id, name, rate):
    return SimpleNamespace(id=row_id, data=SimpleNamespace(name=name, hourlyRateUsd=rate))


def test_lists_jobs_sorted_by_name_with_their_rates(monkeypatch):
    rows = [row("2", "Financial Analyst", 45.0), row("1", "Accountant", 38.0)]
    monkeypatch.setattr(module, "iter_table_rows", lambda table_id, model, queries=None: iter(rows))

    result = module.list_industry_jobs("accounting-finance")

    assert [(job.id, job.name, job.hourly_rate_usd) for job in result] == [
        ("1", "Accountant", 38.0),
        ("2", "Financial Analyst", 45.0),
    ]


def test_asks_only_for_the_jobs_of_the_given_industry(monkeypatch):
    seen = {}

    def fake_iter(table_id, model, queries=None):
        seen["queries"] = queries
        return iter([])

    monkeypatch.setattr(module, "iter_table_rows", fake_iter)

    module.list_industry_jobs("accounting-finance")

    assert "industryId" in seen["queries"][0]
    assert "accounting-finance" in seen["queries"][0]
