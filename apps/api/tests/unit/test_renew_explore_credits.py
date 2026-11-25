from datetime import UTC, datetime

import app.services.subscriptions.renew_explore_credits as module
from tests.conftest import make_subscription

NOW = datetime(2027, 1, 15, 12, 0, tzinfo=UTC)


def test_resets_the_explore_credits_for_the_day_and_remembers_when(monkeypatch):
    calls = []
    monkeypatch.setattr(module, "apply_plan_credits", lambda *args: calls.append(("credits", args)))
    monkeypatch.setattr(
        module, "update_subscription_row", lambda user_id, data: calls.append(("row", data))
    )

    module.renew_explore_credits(make_subscription(plan="explore"), NOW)

    assert calls == [
        ("credits", ("user-1", "explore", "explore:2027-01-15")),
        ("row", {"creditsRenewedAt": NOW.isoformat()}),
    ]
