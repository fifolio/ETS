import pytest
from appwrite.exception import AppwriteException

import app.services.account.user_exists as module


class FakeUsers:
    def __init__(self, error=None):
        self.error = error

    def get(self, user_id):
        if self.error:
            raise self.error
        return object()


def test_true_when_the_user_exists(monkeypatch):
    monkeypatch.setattr(module, "get_users", lambda: FakeUsers())

    assert module.user_exists("user-1") is True


def test_false_when_the_user_was_deleted(monkeypatch):
    monkeypatch.setattr(module, "get_users", lambda: FakeUsers(AppwriteException("missing", 404)))

    assert module.user_exists("user-1") is False


def test_other_errors_are_raised(monkeypatch):
    monkeypatch.setattr(module, "get_users", lambda: FakeUsers(AppwriteException("boom", 500)))

    with pytest.raises(AppwriteException):
        module.user_exists("user-1")
