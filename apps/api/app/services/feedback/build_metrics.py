from app.types.feedback_metrics import FeedbackMetrics
from app.types.usage_stats import UsageStats


def build_metrics(stats: UsageStats) -> FeedbackMetrics:
    return FeedbackMetrics(
        scans=stats.scans,
        words=stats.words,
        minutes_saved=round(stats.minutes, 1),
    )
