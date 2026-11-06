from app.services.feedback.build_metrics import build_metrics
from app.services.usage.get_usage_stats import get_usage_stats
from app.types.feedback_metrics import FeedbackMetrics


def compute_metrics(user_id: str) -> FeedbackMetrics:
    return build_metrics(get_usage_stats(user_id))
