import pytest

import app.services.account.delete_user_data as module
from app.core.config import settings


def install(monkeypatch, fail_on=None):
    calls = []
    monkeypatch.setattr(settings, "appwrite_scans_table_id", "scans-table")
    monkeypatch.setattr(settings, "appwrite_extensions_table_id", "extensions-table")

    def make(name):
        def step(user_id):
            calls.append((name, user_id))
            if name == fail_on:
                raise RuntimeError(f"{name} failed")

        return step

    def rows(table_id, user_id):
        calls.append((table_id, user_id))

    monkeypatch.setattr(module, "delete_cv", make("cv"))
    monkeypatch.setattr(module, "delete_usage_row", make("usage"))
    monkeypatch.setattr(module, "delete_rows_by_user", rows)
    return calls


def test_deletes_the_cv_usage_scans_and_extension_installs(monkeypatch):
    calls = install(monkeypatch)

    module.delete_user_data("user-1")

    assert calls == [
        ("cv", "user-1"),
        ("usage", "user-1"),
        ("scans-table", "user-1"),
        ("extensions-table", "user-1"),
    ]


def test_a_failing_step_raises_so_the_deletion_can_be_retried(monkeypatch):
    install(monkeypatch, fail_on="usage")

    with pytest.raises(RuntimeError):
        module.delete_user_data("user-1")
