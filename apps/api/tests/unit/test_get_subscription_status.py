import app.services.subscriptions.get_subscription_status as module
from app.types.authenticated_user import AuthenticatedUser
from tests.conftest import make_subscription


def make_user(plan):
    return AuthenticatedUser("user-1", "Jane Doe", "jane@example.com", True, {}, [], plan)


def test_reads_the_users_row_and_uses_their_plan(monkeypatch):
    asked = []
    monkeypatch.setattr(
        module,
        "find_subscription_row",
        lambda column, value: asked.append((column, value)) or make_subscription(),
    )

    status = module.get_subscription_status(make_user("nextmove"))

    assert asked == [("$id", "user-1")]
    assert (status.plan, status.can_cancel) == ("nextmove", True)


def test_a_user_without_a_row_is_shown_as_their_plan_with_nothing_to_manage(monkeypatch):
    monkeypatch.setattr(module, "find_subscription_row", lambda column, value: None)

    status = module.get_subscription_status(make_user("explore"))

    assert (status.plan, status.can_manage) == ("explore", False)
