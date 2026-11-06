from dataclasses import dataclass


@dataclass(frozen=True)
class UsageStats:
    scans: int
    words: int
