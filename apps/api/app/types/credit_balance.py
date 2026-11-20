from dataclasses import dataclass


@dataclass(frozen=True)
class CreditBalance:
    subscription: int
    promotional: int
    purchased: int

    @property
    def total(self) -> int:
        return self.subscription + self.promotional + self.purchased
