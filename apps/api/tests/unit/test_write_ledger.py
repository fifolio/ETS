import pytest
from appwrite.exception import AppwriteException

import app.services.credits.write_ledger as module


class FakeTables:
    def __init__(self, error=None):
        self.error = error
        self.calls = []

    def create_row(self, **kwargs):
        self.calls.append(kwargs)
        if self.error:
            raise self.error


def test_stores_the_event_and_returns_its_id(monkeypatch):
    tables = FakeTables()
    monkeypatch.setattr(module, "get_tables_db", lambda: tables)

    row_id = module.write_ledger("user-1", -1, "promotional", "Job scan", None, "key-1")

    assert row_id == tables.calls[0]["row_id"]
    assert tables.calls[0]["data"] == {
        "userId": "user-1",
        "amount": -1,
        "kind": "promotional",
        "reason": "Job scan",
        "refId": None,
        "idempotencyKey": "key-1",
    }


def test_a_key_that_was_already_used_gives_none(monkeypatch):
    monkeypatch.setattr(module, "get_tables_db", lambda: FakeTables(AppwriteException("dup", 409)))

    assert module.write_ledger("user-1", 25, "purchased", "Top-up", None, "key-1") is None


def test_other_errors_are_raised(monkeypatch):
    monkeypatch.setattr(module, "get_tables_db", lambda: FakeTables(AppwriteException("boom", 500)))

    with pytest.raises(AppwriteException):
        module.write_ledger("user-1", 25, "purchased", "Top-up")
