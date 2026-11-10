from types import SimpleNamespace

import app.services.cleanup.find_data_owner_ids as module
from app.core.config import settings


def user_row(user_id):
    return SimpleNamespace(id=f"row-{user_id}", data=SimpleNamespace(userId=user_id))


def usage_row(user_id):
    return SimpleNamespace(id=user_id, data=SimpleNamespace(scanCount=1))


def test_collects_the_owners_of_cvs_usage_rows_and_extension_installs(monkeypatch):
    monkeypatch.setattr(settings, "appwrite_cvs_table_id", "cvs-table")
    monkeypatch.setattr(settings, "appwrite_usage_table_id", "usage-table")
    monkeypatch.setattr(settings, "appwrite_extensions_table_id", "extensions-table")
    rows = {
        "cvs-table": [user_row("u1"), user_row("u2")],
        "usage-table": [usage_row("u2"), usage_row("u3")],
        "extensions-table": [user_row("u4")],
    }
    monkeypatch.setattr(module, "iter_table_rows", lambda table_id, model: iter(rows[table_id]))

    assert module.find_data_owner_ids() == {"u1", "u2", "u3", "u4"}


def test_a_database_without_rows_has_no_owners(monkeypatch):
    monkeypatch.setattr(module, "iter_table_rows", lambda table_id, model: iter([]))

    assert module.find_data_owner_ids() == set()
