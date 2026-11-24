from datetime import datetime

from app.constants.topups import TOPUP_SKU
from app.services.account.user_exists import user_exists
from app.services.credits.ensure_credit_account import ensure_credit_account
from app.services.credits.grant_topup_credits import grant_topup_credits
from app.services.payments.activate_plan import activate_plan
from app.services.payments.judge_payment import judge_payment
from app.services.payments.reject_payment import reject_payment
from app.services.payments.resolve_payment_rows import resolve_payment_rows
from app.services.payments.save_payment_result import save_payment_result
from app.services.plans.find_plan import find_plan
from app.services.topups.credits_for_cents import credits_for_cents
from app.types.payment_notice import PaymentNotice
from app.types.payment_result import PaymentResult
from app.types.payment_verdict import PaymentVerdict


def apply_payment(notice: PaymentNotice, now: datetime) -> str:
    """Apply one confirmed payment, once. Returns what happened."""
    rows = resolve_payment_rows(notice)
    if rows.existing and rows.existing.applied:
        return "duplicate"

    verdict = judge_payment(notice, rows.template)
    if verdict.outcome != "ok":
        return reject_payment(rows.row, notice, verdict, now)
    if not user_exists(notice.user_id):
        unknown = PaymentVerdict("unknown_user", "failed", verdict.expected_cents)
        return reject_payment(rows.row, notice, unknown, now)

    ensure_credit_account(notice.user_id, now)  # the welcome bonus and Explore credits come first
    if notice.sku == TOPUP_SKU:
        credits = credits_for_cents(verdict.expected_cents)
        grant_topup_credits(notice.user_id, verdict.expected_cents, notice.payment_id)
    else:
        plan_id = notice.sku.removeprefix("plan_")
        plan = find_plan(plan_id)
        credits = plan.subscription_credits if plan else 0
        activate_plan(notice, plan_id, now)

    result = PaymentResult(verdict.expected_cents, credits, "completed", True)
    save_payment_result(rows.row, notice, result, now)
    return "applied"
