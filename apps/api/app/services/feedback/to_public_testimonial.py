from app.constants.feedback import TESTIMONIAL_STATUS_APPROVED
from app.schemas.feedback_row import FeedbackRow
from app.schemas.public_testimonial import PublicTestimonial
from app.services.feedback.parse_metrics import parse_metrics


def to_public_testimonial(row_id: str, row: FeedbackRow) -> PublicTestimonial | None:
    """The public version of a row, or None when it must not be shown."""
    quote = (row.quote or "").strip()
    if row.status != TESTIMONIAL_STATUS_APPROVED or not row.consent or not quote:
        return None
    metrics = parse_metrics(row.metricsSaved)
    return PublicTestimonial(
        id=row_id,
        quote=quote,
        display_name=row.displayName or "Anonymous",
        role=row.role or None,
        hours_saved=round(metrics.minutes_saved / 60, 1),
        scans=metrics.scans,
    )
