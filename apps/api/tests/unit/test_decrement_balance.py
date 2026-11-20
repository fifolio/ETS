import pytest
from appwrite.exception import AppwriteException

import app.services.credits.decrement_balance as module


class FakeTables:
    def __init__(self, error=None):
        self.error = error
        self.calls = []

    def decrement_row_column(self, **kwargs):
        self.calls.append(kwargs)
        if self.error:
            raise self.error


def test_takes_credits_from_the_right_column_with_a_minimum_of_zero(monkeypatch):
    tables = FakeTables()
    monkeypatch.setattr(module, "get_tables_db", lambda: tables)

    assert module.decrement_balance("user-1", "promotional", 2) is True

    call = tables.calls[0]
    assert (call["row_id"], call["column"], call["value"], call["min"]) == (
        "user-1",
        "promotionalCredits",
        2,
        0,
    )


@pytest.mark.parametrize("code", [400, 409])
def test_a_column_without_enough_credits_gives_false(monkeypatch, code):
    monkeypatch.setattr(module, "get_tables_db", lambda: FakeTables(AppwriteException("no", code)))

    assert module.decrement_balance("user-1", "subscription", 1) is False


def test_other_errors_are_raised(monkeypatch):
    monkeypatch.setattr(module, "get_tables_db", lambda: FakeTables(AppwriteException("boom", 500)))

    with pytest.raises(AppwriteException):
        module.decrement_balance("user-1", "subscription", 1)
