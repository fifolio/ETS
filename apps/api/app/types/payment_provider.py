from typing import Protocol

from app.types.checkout_order import CheckoutOrder
from app.types.checkout_session import CheckoutSession


class PaymentProvider(Protocol):
    name: str
    environment: str  # for example sandbox or production

    def create_checkout(self, order: CheckoutOrder) -> CheckoutSession:
        """Start a payment for the order and return the provider's checkout."""
        ...
