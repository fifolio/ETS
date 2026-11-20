import pytest
from appwrite.exception import AppwriteException

import app.services.credits.increment_balance as module


class FakeTables:
    def __init__(self, errors=()):
        self.errors = list(errors)
        self.calls = []

    def increment_row_column(self, **kwargs):
        self.calls.append(kwargs)
        error = self.errors.pop(0) if self.errors else None
        if error:
            raise error


def install(monkeypatch, tables, create_error=None):
    created = []

    def create(user_id, kind, amount):
        if create_error:
            raise create_error
        created.append((user_id, kind, amount))

    monkeypatch.setattr(module, "get_tables_db", lambda: tables)
    monkeypatch.setattr(module, "create_balance_row", create)
    return created


def test_adds_to_the_column_of_the_kind_for_that_user(monkeypatch):
    tables = FakeTables()
    install(monkeypatch, tables)

    module.increment_balance("user-1", "purchased", 25)

    call = tables.calls[0]
    assert (call["row_id"], call["column"], call["value"]) == ("user-1", "purchasedCredits", 25)


def test_creates_the_row_on_the_first_grant(monkeypatch):
    created = install(monkeypatch, FakeTables([AppwriteException("missing", 404)]))

    module.increment_balance("user-1", "purchased", 25)

    assert created == [("user-1", "purchased", 25)]


def test_adds_again_when_another_request_created_the_row_first(monkeypatch):
    tables = FakeTables([AppwriteException("missing", 404), None])
    install(monkeypatch, tables, create_error=AppwriteException("exists", 409))

    module.increment_balance("user-1", "purchased", 25)

    assert len(tables.calls) == 2


def test_other_errors_are_raised(monkeypatch):
    install(monkeypatch, FakeTables([AppwriteException("boom", 500)]))

    with pytest.raises(AppwriteException):
        module.increment_balance("user-1", "purchased", 25)
