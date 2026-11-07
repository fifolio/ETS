from types import SimpleNamespace

import app.services.cleanup.find_data_owner_ids as module
from app.core.config import settings


def cv_row(user_id):
    return SimpleNamespace(id=f"row-{user_id}", data=SimpleNamespace(userId=user_id))


def usage_row(user_id):
    return SimpleNamespace(id=user_id, data=SimpleNamespace(scanCount=1, wordsTotal=100))


def test_collects_the_owners_of_cvs_and_usage_rows(monkeypatch):
    monkeypatch.setattr(settings, "appwrite_cvs_table_id", "cvs-table")
    monkeypatch.setattr(settings, "appwrite_usage_table_id", "usage-table")
    rows = {
        "cvs-table": [cv_row("u1"), cv_row("u2")],
        "usage-table": [usage_row("u2"), usage_row("u3")],
    }
    monkeypatch.setattr(module, "iter_table_rows", lambda table_id, model: iter(rows[table_id]))

    assert module.find_data_owner_ids() == {"u1", "u2", "u3"}


def test_a_database_without_rows_has_no_owners(monkeypatch):
    monkeypatch.setattr(module, "iter_table_rows", lambda table_id, model: iter([]))

    assert module.find_data_owner_ids() == set()
