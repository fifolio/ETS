import pytest
from appwrite.exception import AppwriteException

import app.services.appwrite.delete_row_by_id as module


class FakeTables:
    def __init__(self, error=None):
        self.error = error
        self.calls = []

    def delete_row(self, **kwargs):
        self.calls.append(kwargs)
        if self.error:
            raise self.error


def test_deletes_the_row_in_the_given_table(monkeypatch):
    tables = FakeTables()
    monkeypatch.setattr(module, "get_tables_db", lambda: tables)

    module.delete_row_by_id("balances", "user-1")

    assert (tables.calls[0]["table_id"], tables.calls[0]["row_id"]) == ("balances", "user-1")


def test_a_row_that_doesnt_exist_is_fine(monkeypatch):
    monkeypatch.setattr(
        module, "get_tables_db", lambda: FakeTables(AppwriteException("missing", 404))
    )

    module.delete_row_by_id("balances", "user-1")


def test_other_errors_are_raised(monkeypatch):
    monkeypatch.setattr(module, "get_tables_db", lambda: FakeTables(AppwriteException("boom", 500)))

    with pytest.raises(AppwriteException):
        module.delete_row_by_id("balances", "user-1")
