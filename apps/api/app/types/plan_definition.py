from dataclasses import dataclass


@dataclass(frozen=True)
class PlanDefinition:
    id: str
    name: str
    price_usd_per_month: float | None
