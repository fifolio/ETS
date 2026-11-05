import app.services.account.mark_cv_done as mark_cv_done_module
import app.services.appwrite.add_user_label as add_user_label_module
from app.services.account.mark_cv_done import mark_cv_done
from app.services.appwrite.add_user_label import add_user_label
from app.types.authenticated_user import AuthenticatedUser


class FakeUsers:
    def __init__(self):
        self.calls = []

    def update_labels(self, user_id, labels):
        self.calls.append((user_id, labels))


def make_user(labels):
    return AuthenticatedUser("user-1", "Jane Doe", "jane.doe@example.com", True, {}, labels)


def test_adding_a_label_keeps_the_existing_ones(monkeypatch):
    users = FakeUsers()
    monkeypatch.setattr(add_user_label_module, "get_users", lambda: users)

    add_user_label("user-1", ["nextmove"], "cvdone")

    assert users.calls == [("user-1", ["cvdone", "nextmove"])]


def test_mark_cv_done_adds_the_label_once(monkeypatch):
    calls = []
    monkeypatch.setattr(mark_cv_done_module, "add_user_label", lambda *args: calls.append(args))

    mark_cv_done(make_user(["nextmove"]))

    assert calls == [("user-1", ["nextmove"], "cvdone")]


def test_mark_cv_done_does_nothing_when_the_label_exists(monkeypatch):
    calls = []
    monkeypatch.setattr(mark_cv_done_module, "add_user_label", lambda *args: calls.append(args))

    mark_cv_done(make_user(["cvdone"]))

    assert calls == []
