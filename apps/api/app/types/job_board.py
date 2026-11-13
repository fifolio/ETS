from dataclasses import dataclass


@dataclass(frozen=True)
class JobBoard:
    id: str
    name: str
    url: str
    min_plan: str
