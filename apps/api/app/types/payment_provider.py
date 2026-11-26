from typing import Protocol

from app.types.checkout_order import CheckoutOrder
from app.types.checkout_session import CheckoutSession


class PaymentProvider(Protocol):
    name: str
    environment: str  # for example sandbox or production

    def create_checkout(self, order: CheckoutOrder) -> CheckoutSession:
        """Start a payment for the order and return the provider's checkout."""
        ...

    def cancel_subscription(self, subscription_id: str) -> None:
        """Immediately end a subscription and stop billing."""
        ...

    def get_manage_url(self, subscription_id: str) -> str | None:
        """The provider's billing page for a subscription, or None."""
        ...
