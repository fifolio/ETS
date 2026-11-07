import pytest

import app.services.account.delete_user_account as module


def test_deletes_the_data_before_the_account(monkeypatch):
    order = []
    monkeypatch.setattr(module, "delete_user_data", lambda user_id: order.append(("data", user_id)))
    monkeypatch.setattr(
        module, "delete_appwrite_user", lambda user_id: order.append(("user", user_id))
    )

    module.delete_user_account("user-1")

    assert order == [("data", "user-1"), ("user", "user-1")]


def test_keeps_the_account_when_deleting_the_data_fails(monkeypatch):
    deleted = []

    def fail(user_id):
        raise RuntimeError("storage down")

    monkeypatch.setattr(module, "delete_user_data", fail)
    monkeypatch.setattr(module, "delete_appwrite_user", deleted.append)

    with pytest.raises(RuntimeError):
        module.delete_user_account("user-1")
    assert deleted == []
