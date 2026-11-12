from dataclasses import dataclass


@dataclass(frozen=True)
class PlanDefinition:
    id: str
    name: str
    max_job_boards: int | None  # None means all of them
    price_usd_per_month: float | None  # None means the price is not set
