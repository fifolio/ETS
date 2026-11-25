from typing import Any

from app.services.appwrite.parse_optional_datetime import parse_optional_datetime
from app.types.membership_notice import MembershipNotice


def parse_whop_membership(data: dict[str, Any]) -> MembershipNotice | None:
    membership_id = data.get("id")
    if not isinstance(membership_id, str) or not membership_id:
        return None
    # Whop's API generations name the period end differently: read either.
    period_end = data.get("current_period_end") or data.get("renewal_period_end")
    return MembershipNotice(
        provider="whop",
        membership_id=membership_id,
        status=str(data.get("status") or ""),
        cancel_at_period_end=bool(data.get("cancel_at_period_end")),
        period_end=parse_optional_datetime(period_end),
    )
