from types import SimpleNamespace

import app.services.subscriptions.find_subscription_row as module


class FakeTables:
    def __init__(self, rows):
        self.rows = rows
        self.queries = None

    def list_rows(self, **kwargs):
        self.queries = kwargs["queries"]
        return SimpleNamespace(rows=self.rows)


def row(**overrides):
    data = {
        "plan": "nextmove",
        "status": "active",
        "cancelAtPeriodEnd": True,
        "providerSubscriptionId": "mem_1",
        "currentPeriodEnd": "2026-12-31T00:00:00.000Z",
        "creditsRenewedAt": None,
        "renewalReminderSentAt": None,
    }
    return SimpleNamespace(id="user-1", data=SimpleNamespace(**{**data, **overrides}))


def test_maps_the_row_and_asks_for_the_column_and_value(monkeypatch):
    tables = FakeTables([row()])
    monkeypatch.setattr(module, "get_tables_db", lambda: tables)

    record = module.find_subscription_row("providerSubscriptionId", "mem_1")

    assert (record.user_id, record.plan, record.membership_id, record.cancel_at_period_end) == (
        "user-1",
        "nextmove",
        "mem_1",
        True,
    )
    assert record.period_end.year == 2026 and record.reminder_sent_at is None
    assert "providerSubscriptionId" in " ".join(tables.queries)


def test_an_explore_row_has_no_membership_and_no_dates(monkeypatch):
    explore = row(plan="explore", providerSubscriptionId=None, currentPeriodEnd=None)
    monkeypatch.setattr(module, "get_tables_db", lambda: FakeTables([explore]))

    record = module.find_subscription_row("$id", "user-1")

    assert (record.membership_id, record.period_end) == (None, None)


def test_no_row_gives_none(monkeypatch):
    monkeypatch.setattr(module, "get_tables_db", lambda: FakeTables([]))

    assert module.find_subscription_row("$id", "nobody") is None
