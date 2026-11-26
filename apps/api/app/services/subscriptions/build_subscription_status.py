from app.constants.plans import PLANS
from app.schemas.subscription_out import SubscriptionOut
from app.services.plans.find_plan import find_plan
from app.types.subscription_record import SubscriptionRecord


def build_subscription_status(plan_id: str, record: SubscriptionRecord | None) -> SubscriptionOut:
    """What Settings shows. The plan comes from the user's label (what access uses)."""
    plan = find_plan(plan_id) or PLANS[0]
    paid = plan.id != "explore"
    has_membership = bool(record and record.membership_id)
    cancelling = bool(record and record.cancel_at_period_end)
    period_end = record.period_end if record and paid else None
    return SubscriptionOut(
        plan=plan.id,
        plan_name=plan.name,
        is_paid=paid,
        current_period_end=period_end.isoformat() if period_end else None,
        cancel_at_period_end=paid and cancelling,
        can_manage=paid and has_membership,
        can_cancel=paid and has_membership and not cancelling,
    )
