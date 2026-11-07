import pytest

import app.services.account.delete_user_data as module


def install(monkeypatch, fail_on=None):
    calls = []

    def make(name):
        def step(user_id):
            calls.append((name, user_id))
            if name == fail_on:
                raise RuntimeError(f"{name} failed")

        return step

    monkeypatch.setattr(module, "delete_cv", make("cv"))
    monkeypatch.setattr(module, "delete_usage_row", make("usage"))
    monkeypatch.setattr(module, "delete_user_scans", make("scans"))
    return calls


def test_deletes_the_cv_the_usage_totals_and_the_scans(monkeypatch):
    calls = install(monkeypatch)

    module.delete_user_data("user-1")

    assert calls == [("cv", "user-1"), ("usage", "user-1"), ("scans", "user-1")]


def test_a_failing_step_raises_so_the_deletion_can_be_retried(monkeypatch):
    install(monkeypatch, fail_on="usage")

    with pytest.raises(RuntimeError):
        module.delete_user_data("user-1")
