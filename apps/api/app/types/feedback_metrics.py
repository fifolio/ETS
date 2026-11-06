from dataclasses import dataclass


@dataclass(frozen=True)
class FeedbackMetrics:
    scans: int
    words: int
    minutes_saved: float
