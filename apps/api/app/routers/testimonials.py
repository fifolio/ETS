from typing import Annotated

from fastapi import APIRouter, Query, Response

from app.constants.feedback import DEFAULT_PUBLIC_LIMIT, MAX_PUBLIC_LIMIT
from app.schemas.public_testimonial import PublicTestimonial
from app.services.feedback.list_approved_testimonials import list_approved_testimonials

router = APIRouter(tags=["testimonials"])


@router.get(
    "/testimonials",
    response_model=list[PublicTestimonial],
    summary="Approved testimonials for the landing page",
    description="Public. Only approved testimonials with consent. \
        Internal suggestions are never included.",
)
def public_testimonials(
    response: Response,
    limit: Annotated[int, Query(ge=1, le=MAX_PUBLIC_LIMIT)] = DEFAULT_PUBLIC_LIMIT,
) -> list[PublicTestimonial]:
    response.headers["Cache-Control"] = "public, max-age=300"
    return list_approved_testimonials(limit)
