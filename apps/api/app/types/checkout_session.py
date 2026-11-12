from dataclasses import dataclass


@dataclass(frozen=True)
class CheckoutSession:
    url: str  # where to send the user to pay
    reference: str  # the provider's own ID for this payment
