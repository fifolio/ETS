from dataclasses import dataclass


@dataclass(frozen=True)
class UsageStats:
    scans: int
    words: int
    minutes: float = 0.0
    cash: float = 0.0
