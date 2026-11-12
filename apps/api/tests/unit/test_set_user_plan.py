from types import SimpleNamespace

import app.services.account.set_user_plan as module


class FakeUsers:
    def __init__(self, labels):
        self.labels = labels
        self.updates = []

    def get(self, user_id):
        return SimpleNamespace(labels=self.labels)

    def update_labels(self, user_id, labels):
        self.updates.append((user_id, labels))


def test_sets_the_plan_label_and_keeps_the_other_labels(monkeypatch):
    users = FakeUsers(["cvdone", "feedbackdone"])
    monkeypatch.setattr(module, "get_users", lambda: users)

    module.set_user_plan("user-1", "nextmove")

    assert users.updates == [("user-1", ["cvdone", "feedbackdone", "nextmove"])]


def test_going_back_to_explore_removes_the_plan_label(monkeypatch):
    users = FakeUsers(["urgent", "cvdone"])
    monkeypatch.setattr(module, "get_users", lambda: users)

    module.set_user_plan("user-1", "explore")

    assert users.updates == [("user-1", ["cvdone"])]
