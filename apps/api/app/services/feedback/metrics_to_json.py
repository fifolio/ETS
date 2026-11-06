import json
from dataclasses import asdict

from app.types.feedback_metrics import FeedbackMetrics


def metrics_to_json(metrics: FeedbackMetrics) -> str:
    return json.dumps(asdict(metrics))
