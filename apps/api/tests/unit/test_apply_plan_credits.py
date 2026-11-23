import pytest

import app.services.credits.apply_plan_credits as module


def install(monkeypatch, grant_result=True):
    calls = []
    monkeypatch.setattr(
        module,
        "expire_monthly_credits",
        lambda user_id, key: calls.append(("expire", user_id, key)),
    )
    monkeypatch.setattr(
        module, "add_credits", lambda *args: calls.append(("grant", args)) or grant_result
    )
    return calls


def test_expires_the_leftover_then_grants_the_plans_monthly_allowance(monkeypatch):
    calls = install(monkeypatch)

    assert module.apply_plan_credits("user-1", "nextmove", "2026-12-01") is True

    base = "plan-credits:user-1:nextmove:2026-12-01"
    assert calls == [
        ("expire", "user-1", f"{base}:expire"),
        ("grant", ("user-1", "subscription", 150, "Next Move monthly credits", f"{base}:grant")),
    ]


def test_it_never_grants_the_welcome_bonus(monkeypatch):
    calls = install(monkeypatch)

    for plan in ("explore", "nextmove", "urgent"):
        module.apply_plan_credits("user-1", plan, "p1")

    assert {call[1][1] for call in calls if call[0] == "grant"} == {"subscription"}


def test_a_period_that_was_already_applied_reports_false(monkeypatch):
    install(monkeypatch, grant_result=False)

    assert module.apply_plan_credits("user-1", "nextmove", "p1") is False


def test_an_unknown_plan_is_refused_before_anything_changes(monkeypatch):
    calls = install(monkeypatch)

    with pytest.raises(ValueError):
        module.apply_plan_credits("user-1", "platinum", "p1")
    assert calls == []
