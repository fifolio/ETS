from typing import Any

from app.constants.topups import TOPUP_SKU
from app.core.config import settings
from app.exceptions.configuration_error import ConfigurationError
from app.services.payments.whop.get_whop_settings import get_whop_settings
from app.services.payments.whop.parse_checkout_configuration import parse_checkout_configuration
from app.services.payments.whop.post_checkout_configuration import post_checkout_configuration
from app.services.payments.whop.post_cancel_membership import post_cancel_membership
from app.types.checkout_order import CheckoutOrder
from app.types.checkout_session import CheckoutSession


class WhopProvider:
    name = "whop"

    @property
    def environment(self) -> str:
        return settings.whop_environment

    def create_checkout(self, order: CheckoutOrder) -> CheckoutSession:
        whop = get_whop_settings()
        body: dict[str, Any] = {
            # Whop copies this onto the payment, so the webhook can tell who bought what.
            "metadata": {"ets_user_id": order.user_id, "ets_sku": order.sku},
            "redirect_url": settings.payment_success_url,
        }
        plan_id: str | None = None
        if order.sku == TOPUP_SKU:
            variant: dict[str, Any] = {
                "billing_type": "one_time",
                "currency": "usd",
                "initial_price": order.amount_cents / 100,  # dollars, as Whop expects
                "title": f"ETS credits ({order.credits})",
                "description": f"{order.credits} ETS credits",
            }
            if whop.topup_product_id:
                variant["product_id"] = whop.topup_product_id
            body["variant"] = variant
        else:
            plan_id = whop.plan_ids.get(order.sku)
            if not plan_id:
                raise ConfigurationError(f"No Whop plan is set for {order.sku}")
            body["variant_id"] = plan_id

        data = post_checkout_configuration(whop, body)
        checkout_id, url, resolved_plan_id = parse_checkout_configuration(data, whop, plan_id)
        return CheckoutSession(checkout_id=checkout_id, plan_id=resolved_plan_id, url=url)

    def cancel_subscription(self, subscription_id: str) -> None:
        post_cancel_membership(get_whop_settings(), subscription_id)
