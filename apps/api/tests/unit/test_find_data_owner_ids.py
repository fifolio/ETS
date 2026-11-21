from types import SimpleNamespace

import app.services.cleanup.find_data_owner_ids as module
from app.core.config import settings


def user_row(user_id):
    return SimpleNamespace(id=f"row-{user_id}", data=SimpleNamespace(userId=user_id))


def usage_row(user_id):
    return SimpleNamespace(id=user_id, data=SimpleNamespace(scanCount=1))


def test_collects_the_owners_of_every_table_that_holds_personal_data(monkeypatch):
    monkeypatch.setattr(settings, "appwrite_cvs_table_id", "cvs-table")
    monkeypatch.setattr(settings, "appwrite_usage_table_id", "usage-table")
    monkeypatch.setattr(settings, "appwrite_extensions_table_id", "extensions-table")
    monkeypatch.setattr(settings, "appwrite_suggestions_table_id", "suggestions-table")
    monkeypatch.setattr(settings, "appwrite_credit_balances_table_id", "balances-table")
    rows = {
        "cvs-table": [user_row("u1"), user_row("u2")],
        "usage-table": [usage_row("u2"), usage_row("u3")],
        "extensions-table": [user_row("u4")],
        "suggestions-table": [user_row("u5"), user_row("u1")],
        "balances-table": [usage_row("u6")],
    }
    monkeypatch.setattr(module, "iter_table_rows", lambda table_id, model: iter(rows[table_id]))

    assert module.find_data_owner_ids() == {"u1", "u2", "u3", "u4", "u5", "u6"}


def test_a_database_without_rows_has_no_owners(monkeypatch):
    monkeypatch.setattr(module, "iter_table_rows", lambda table_id, model: iter([]))

    assert module.find_data_owner_ids() == set()
