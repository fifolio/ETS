from datetime import UTC, datetime

from app.services.payments.whop.parse_whop_membership import parse_whop_membership


def test_reads_the_membership_with_the_current_period_end():
    notice = parse_whop_membership(
        {
            "id": "mem_1",
            "status": "active",
            "cancel_at_period_end": True,
            "current_period_end": "2026-12-31T00:00:00.000Z",
        }
    )

    assert (notice.membership_id, notice.status, notice.cancel_at_period_end) == (
        "mem_1",
        "active",
        True,
    )
    assert notice.period_end == datetime(2026, 12, 31, tzinfo=UTC)


def test_reads_the_other_name_of_the_period_end_too():
    notice = parse_whop_membership(
        {"id": "mem_1", "status": "active", "renewal_period_end": "2026-12-31T00:00:00Z"}
    )

    assert notice.period_end == datetime(2026, 12, 31, tzinfo=UTC)


def test_a_membership_without_period_end_or_flags_has_safe_defaults():
    notice = parse_whop_membership({"id": "mem_1", "status": "canceled"})

    assert (notice.cancel_at_period_end, notice.period_end) == (False, None)


def test_data_without_an_id_is_refused():
    assert parse_whop_membership({"status": "active"}) is None
