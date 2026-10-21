import logging

from fastapi import APIRouter, HTTPException

from app.chains.matcher import analyze
from app.schemas.analyze import AnalyzeRequest
from app.schemas.errors import ErrorResponse
from app.schemas.verdict import MatchResult

logger = logging.getLogger(__name__)

router = APIRouter(
    tags=["analyze"],
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request - Invalid input data."},
        422: {"model": ErrorResponse, "description": "Unprocessable Entity - Validation error."},
        503: {
            "model": ErrorResponse,
            "description": "Service Unavailable - The AI service is unavailable.",
        },
        502: {
            "model": ErrorResponse,
            "description": "Bad Gateway - An unexpected error occurred during analysis.",
        },
    },
)


@router.post(
    "/analyze",
    response_model=MatchResult,
    response_description="Verdict, score, and reasons for the match.",
    summary="Analyze a candidate's CV against a job post",
    description="This endpoint takes the plain text of a candidate's CV \
        and the text of a job post, and returns a match result indicating "
    "how well the candidate's qualifications align with the job requirements.",
)
def analyze_job(payload: AnalyzeRequest) -> MatchResult:
    """
    Analyze a candidate's CV against a job post.

    - **cv_text**: Plain text of the candidate's CV
    (min 100 characters, max 20,000 characters)
    - **job_text**: Text of the job post
    (min 50 characters, max 50,000 characters)

    Returns a match result indicating how well the
    candidate's qualifications align with the job requirements.
    """
    try:
        return analyze(payload.cv_text, payload.job_text)
    except RuntimeError as exc:
        logger.error("AI service is not configured or failed to respond: %s", exc)
        raise HTTPException(status_code=503, detail="The AI service is unavailable.") from exc
    except Exception as exc:
        logger.exception("An unexpected error occurred during analysis: %s", exc)
        raise HTTPException(
            status_code=502, detail="An unexpected error occurred during analysis."
        ) from exc
