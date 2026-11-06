from appwrite.query import Query

from app.constants.feedback import TESTIMONIAL_STATUS_APPROVED
from app.core.config import settings
from app.schemas.feedback_row import FeedbackRow
from app.schemas.public_testimonial import PublicTestimonial
from app.services.appwrite.get_tables_db import get_tables_db
from app.services.feedback.to_public_testimonial import to_public_testimonial


def list_approved_testimonials(limit: int) -> list[PublicTestimonial]:
    result = get_tables_db().list_rows(
        database_id=settings.appwrite_database_id,
        table_id=settings.appwrite_testimonials_table_id,
        queries=[
            Query.equal("status", TESTIMONIAL_STATUS_APPROVED),
            Query.order_desc("$createdAt"),
            Query.limit(limit),
        ],
        model_type=FeedbackRow,
    )
    items = (to_public_testimonial(row.id, row.data) for row in result.rows)
    return [item for item in items if item is not None]
