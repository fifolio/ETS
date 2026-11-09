from dataclasses import dataclass


@dataclass(frozen=True)
class ScanSavings:
    minutes: float
    cash: float
