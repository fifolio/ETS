from app.exceptions.payments_unavailable_error import PaymentsUnavailableError
from app.types.checkout_order import CheckoutOrder
from app.types.checkout_session import CheckoutSession


class DisabledProvider:
    """Used until a real payment provider is configured."""

    name = "none"
    environment = "none"

    def create_checkout(self, order: CheckoutOrder) -> CheckoutSession:
        raise PaymentsUnavailableError("No payment provider is configured")

    def cancel_subscription(self, subscription_id: str) -> None:
        raise PaymentsUnavailableError("No payment provider is configured")

    def get_manage_url(self, subscription_id: str) -> str | None:
        raise PaymentsUnavailableError("No payment provider is configured")
