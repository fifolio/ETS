from datetime import datetime

from app.constants.topups import TOPUP_SKU
from app.services.credits.revoke_credits import revoke_credits
from app.services.payments.end_subscription import end_subscription
from app.services.payments.find_payment_row import find_payment_row
from app.services.payments.update_payment_row import update_payment_row
from app.services.subscriptions.find_subscription_row import find_subscription_row
from app.services.topups.credits_for_cents import credits_for_cents
from app.types.refund_notice import RefundNotice


def apply_refund(notice: RefundNotice, now: datetime) -> str:
    """Take back what a successful refund pays for. Once per refund."""
    if notice.status != "succeeded" or notice.amount_cents is None:
        return "ignored"  # a pending refund is acted on when it succeeds
    row = find_payment_row("providerPaymentId", notice.payment_id)
    if row is None or not row.applied:
        return "ignored"  # not one of our payments, or nothing was granted
    if row.status == "refunded":
        return "duplicate"

    full = notice.amount_cents >= row.amount_cents
    if row.sku == TOPUP_SKU:
        credits = credits_for_cents(min(notice.amount_cents, row.amount_cents))
        if credits > 0:
            revoke_credits(
                row.user_id,
                "purchased",
                credits,
                "Refund of a credit top-up",
                f"refund:{notice.refund_id}",
            )
    elif full and notice.membership_id:
        record = find_subscription_row("providerSubscriptionId", notice.membership_id)
        if record is not None:
            end_subscription(record, now)

    if full and row.status != "refunded":
        update_payment_row(row.row_id, {"status": "refunded"})
    return "refunded"
