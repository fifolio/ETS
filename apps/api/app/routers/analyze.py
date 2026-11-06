import logging

from fastapi import APIRouter, HTTPException

from app.chains.analyze import analyze
from app.schemas.analyze_request import AnalyzeRequest
from app.schemas.error_response import ErrorResponse
from app.schemas.match_result import MatchResult
from app.services.cv.get_cv import get_cv
from app.services.scans.save_scan import save_scan
from app.services.text.count_words import count_words
from app.services.usage.record_scan_usage import record_scan_usage
from app.types.verified_user import VerifiedUserId

logger = logging.getLogger(__name__)

router = APIRouter(
    tags=["analyze"],
    responses={
        401: {"model": ErrorResponse, "description": "Missing or invalid token."},
        404: {"model": ErrorResponse, "description": "The user hasn't uploaded a CV yet."},
        422: {"description": "Invalid input: the job text is missing, too short, or too long."},
        502: {"model": ErrorResponse, "description": "The AI model or storage failed."},
        503: {"model": ErrorResponse, "description": "The service is unavailable."},
    },
)


@router.post(
    "/analyze",
    response_model=MatchResult,
    response_description="Verdict, score, and reasons for the match.",
    summary="Smash or pass a job post",
    description="Compares the logged-in user's stored CV with a job post.",
)
def analyze_job(payload: AnalyzeRequest, user_id: VerifiedUserId) -> MatchResult:
    cv = get_cv(user_id)
    if cv is None:
        raise HTTPException(status_code=404, detail="Upload your CV before scanning a job.")

    try:
        result = analyze(cv.text, payload.job_text)
    except RuntimeError as exc:
        logger.error("AI service is not configured: %s", exc)
        raise HTTPException(status_code=503, detail="The AI service is unavailable.") from exc
    except Exception as exc:
        logger.exception("Analysis failed")
        raise HTTPException(
            status_code=502, detail="The AI model failed to respond. Please try again."
        ) from exc

    words = count_words(payload.job_text)

    try:
        save_scan(user_id, result, payload.job_url, payload.job_title, words)
    except Exception:
        # History is a bonus: never lose the verdict because saving it failed.
        logger.exception("Could not save scan history")

    try:
        record_scan_usage(user_id, words)
    except Exception:
        logger.exception("Could not record usage")

    return result
