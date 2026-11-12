from collections.abc import Mapping
from typing import Protocol

from app.types.checkout_session import CheckoutSession
from app.types.payment_event import PaymentEvent
from app.types.plan_definition import PlanDefinition


class PaymentProvider(Protocol):
    name: str

    def create_checkout(self, user_id: str, email: str, plan: PlanDefinition) -> CheckoutSession:
        """Start a payment for the plan and return where to send the user."""
        ...

    def parse_webhook(self, headers: Mapping[str, str], body: bytes) -> PaymentEvent | None:
        """Verify and read a notification from the provider. None for events we ignore."""
        ...
