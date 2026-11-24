from app.constants.topups import TOPUP_SKU
from app.exceptions.checkout_refused_error import CheckoutRefusedError
from app.services.plans.find_plan import find_plan
from app.services.topups.validate_topup_amount import validate_topup_amount
from app.types.payment_notice import PaymentNotice
from app.types.payment_record import PaymentRecord


def get_expected_cents(notice: PaymentNotice, template: PaymentRecord | None) -> int | None:
    """What this purchase should have cost: our record of the checkout, else the catalog."""
    if template is not None and template.amount_cents > 0:
        return template.amount_cents
    if notice.sku == TOPUP_SKU:
        if notice.paid_cents is None:
            return None
        try:
            return validate_topup_amount(notice.paid_cents / 100)
        except CheckoutRefusedError:
            return None
    if notice.sku.startswith("plan_"):
        plan = find_plan(notice.sku.removeprefix("plan_"))
        return round(plan.price_usd_per_month * 100) if plan else None
    return None
