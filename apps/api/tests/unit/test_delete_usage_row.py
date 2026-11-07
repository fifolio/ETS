import pytest
from appwrite.exception import AppwriteException

import app.services.usage.delete_usage_row as module


class FakeTables:
    def __init__(self, error=None):
        self.error = error
        self.calls = []

    def delete_row(self, **kwargs):
        self.calls.append(kwargs)
        if self.error:
            raise self.error


def test_deletes_the_row_that_has_the_user_id(monkeypatch):
    tables = FakeTables()
    monkeypatch.setattr(module, "get_tables_db", lambda: tables)

    module.delete_usage_row("user-1")

    assert tables.calls[0]["row_id"] == "user-1"


def test_a_user_without_usage_is_not_an_error(monkeypatch):
    monkeypatch.setattr(
        module, "get_tables_db", lambda: FakeTables(AppwriteException("missing", 404))
    )

    module.delete_usage_row("user-1")


def test_other_errors_are_raised(monkeypatch):
    monkeypatch.setattr(module, "get_tables_db", lambda: FakeTables(AppwriteException("boom", 500)))

    with pytest.raises(AppwriteException):
        module.delete_usage_row("user-1")
