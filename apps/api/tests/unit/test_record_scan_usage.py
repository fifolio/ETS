import pytest
from appwrite.exception import AppwriteException

import app.services.usage.record_scan_usage as module


class Fakes:
    def __init__(self, increments, create=None):
        self.outcomes = list(increments)  # one entry per increment call: None or an error
        self.create_error = create
        self.increments = []
        self.creates = []

    def increment(self, user_id, words):
        self.increments.append((user_id, words))
        outcome = self.outcomes.pop(0)
        if outcome:
            raise outcome

    def create(self, user_id, words):
        self.creates.append((user_id, words))
        if self.create_error:
            raise self.create_error


def install(monkeypatch, increments, create=None):
    fakes = Fakes(increments, create)
    monkeypatch.setattr(module, "increment_usage", fakes.increment)
    monkeypatch.setattr(module, "create_usage_row", fakes.create)
    return fakes


def test_increments_an_existing_row(monkeypatch):
    fakes = install(monkeypatch, [None])

    module.record_scan_usage("user-1", 900)

    assert fakes.increments == [("user-1", 900)]
    assert fakes.creates == []


def test_creates_the_row_on_the_first_scan(monkeypatch):
    fakes = install(monkeypatch, [AppwriteException("missing", 404)])

    module.record_scan_usage("user-1", 900)

    assert fakes.creates == [("user-1", 900)]


def test_increments_again_when_another_request_created_the_row_first(monkeypatch):
    fakes = install(
        monkeypatch,
        [AppwriteException("missing", 404), None],
        create=AppwriteException("exists", 409),
    )

    module.record_scan_usage("user-1", 900)

    assert len(fakes.increments) == 2


def test_other_errors_are_raised(monkeypatch):
    install(monkeypatch, [AppwriteException("boom", 500)])

    with pytest.raises(AppwriteException):
        module.record_scan_usage("user-1", 900)


def test_a_failed_create_is_raised(monkeypatch):
    install(monkeypatch, [AppwriteException("missing", 404)], create=AppwriteException("boom", 500))

    with pytest.raises(AppwriteException):
        module.record_scan_usage("user-1", 900)
