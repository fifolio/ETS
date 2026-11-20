from datetime import UTC, datetime

import pytest
from appwrite.exception import AppwriteException

import app.services.subscriptions.create_subscription_row as module

NOW = datetime(2026, 11, 20, 12, 0, tzinfo=UTC)


class FakeTables:
    def __init__(self, error=None):
        self.error = error
        self.calls = []

    def create_row(self, **kwargs):
        self.calls.append(kwargs)
        if self.error:
            raise self.error


def test_creates_an_active_row_with_the_user_id_as_its_id(monkeypatch):
    tables = FakeTables()
    monkeypatch.setattr(module, "get_tables_db", lambda: tables)

    module.create_subscription_row("user-1", "explore", NOW)

    call = tables.calls[0]
    assert call["row_id"] == "user-1"
    assert call["data"]["plan"] == "explore" and call["data"]["status"] == "active"
    assert call["data"]["creditsRenewedAt"] == NOW.isoformat()


def test_an_existing_row_is_left_alone(monkeypatch):
    monkeypatch.setattr(
        module, "get_tables_db", lambda: FakeTables(AppwriteException("exists", 409))
    )

    module.create_subscription_row("user-1", "explore", NOW)


def test_other_errors_are_raised(monkeypatch):
    monkeypatch.setattr(module, "get_tables_db", lambda: FakeTables(AppwriteException("boom", 500)))

    with pytest.raises(AppwriteException):
        module.create_subscription_row("user-1", "explore", NOW)
