from app.services.subscriptions.build_subscription_status import build_subscription_status
from tests.conftest import make_subscription


def test_an_explore_user_has_no_renewal_and_nothing_to_manage():
    status = build_subscription_status("explore", None)

    assert (status.plan, status.plan_name, status.is_paid) == ("explore", "Explore", False)
    assert (status.current_period_end, status.can_manage, status.can_cancel) == (None, False, False)


def test_a_paid_plan_shows_its_period_end_and_can_be_managed_and_cancelled():
    status = build_subscription_status("nextmove", make_subscription())

    assert (status.is_paid, status.current_period_end) == (True, "2026-12-31T00:00:00+00:00")
    assert (status.cancel_at_period_end, status.can_manage, status.can_cancel) == (
        False,
        True,
        True,
    )


def test_a_plan_cancelled_at_period_end_cannot_be_cancelled_again():
    status = build_subscription_status("nextmove", make_subscription(cancel_at_period_end=True))

    assert (status.cancel_at_period_end, status.can_manage, status.can_cancel) == (
        True,
        True,
        False,
    )


def test_a_paid_plan_without_a_membership_cannot_be_managed_or_cancelled():
    status = build_subscription_status("urgent", make_subscription(membership_id=None))

    assert (status.can_manage, status.can_cancel) == (False, False)


def test_the_label_decides_the_plan_even_when_the_row_still_says_explore():
    status = build_subscription_status(
        "urgent", make_subscription(plan="explore", membership_id=None, period_end=None)
    )

    assert (status.plan, status.is_paid, status.current_period_end) == ("urgent", True, None)
