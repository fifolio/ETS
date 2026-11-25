from typing import Any

from app.services.payments.whop.money_to_cents import money_to_cents
from app.types.refund_notice import RefundNotice


def parse_whop_refund(data: dict[str, Any]) -> RefundNotice | None:
    refund_id = data.get("id")
    payment = data.get("payment")
    payment = payment if isinstance(payment, dict) else {}
    payment_id = payment.get("id")
    if not (
        isinstance(refund_id, str) and refund_id and isinstance(payment_id, str) and payment_id
    ):
        return None
    membership = payment.get("membership")
    membership_id = membership.get("id") if isinstance(membership, dict) else None
    return RefundNotice(
        provider="whop",
        refund_id=refund_id,
        payment_id=payment_id,
        membership_id=membership_id if isinstance(membership_id, str) else None,
        amount_cents=money_to_cents({"amount": data.get("amount")}),  # Whop writes dollars
        status=str(data.get("status") or ""),
    )
