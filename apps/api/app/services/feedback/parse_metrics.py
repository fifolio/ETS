import json

from app.types.feedback_metrics import FeedbackMetrics


def parse_metrics(text: str | None) -> FeedbackMetrics:
    """Read the stored metrics, falling back to zeros for anything unreadable."""
    try:
        data = json.loads(text or "")
        return FeedbackMetrics(
            scans=int(data["scans"]),
            words=int(data["words"]),
            minutes_saved=float(data["minutes_saved"]),
        )
    except (ValueError, KeyError, TypeError):
        return FeedbackMetrics(scans=0, words=0, minutes_saved=0.0)
