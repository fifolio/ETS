from types import SimpleNamespace

import pytest

import app.services.appwrite.delete_rows_by_user as module
from app.exceptions.data_deletion_error import DataDeletionError


class FakeTables:
    def __init__(self, remaining):
        self.remaining = list(remaining)  # rows left after each delete round
        self.delete_calls = []

    def delete_rows(self, **kwargs):
        self.delete_calls.append(kwargs["table_id"])

    def list_rows(self, **kwargs):
        rows = self.remaining.pop(0) if len(self.remaining) > 1 else self.remaining[0]
        return SimpleNamespace(rows=rows)


def test_one_round_is_enough_when_nothing_remains(monkeypatch):
    tables = FakeTables([[]])
    monkeypatch.setattr(module, "get_tables_db", lambda: tables)

    module.delete_rows_by_user("scans", "user-1")

    assert tables.delete_calls == ["scans"]


def test_repeats_while_rows_remain(monkeypatch):
    tables = FakeTables([[object()], []])
    monkeypatch.setattr(module, "get_tables_db", lambda: tables)

    module.delete_rows_by_user("extensions", "user-1")

    assert tables.delete_calls == ["extensions", "extensions"]


def test_gives_up_after_too_many_rounds(monkeypatch):
    tables = FakeTables([[object()]])
    monkeypatch.setattr(module, "get_tables_db", lambda: tables)
    monkeypatch.setattr(module, "MAX_DELETE_ROUNDS", 2)

    with pytest.raises(DataDeletionError):
        module.delete_rows_by_user("scans", "user-1")
    assert len(tables.delete_calls) == 2
