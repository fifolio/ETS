from collections.abc import Mapping

from app.exceptions.payments_unavailable_error import PaymentsUnavailableError
from app.types.checkout_session import CheckoutSession
from app.types.payment_event import PaymentEvent
from app.types.plan_definition import PlanDefinition


class DisabledProvider:
    """Used until a real payment provider is configured."""

    name = "none"

    def create_checkout(self, user_id: str, email: str, plan: PlanDefinition) -> CheckoutSession:
        raise PaymentsUnavailableError("No payment provider is configured")

    def parse_webhook(self, headers: Mapping[str, str], body: bytes) -> PaymentEvent | None:
        return None
