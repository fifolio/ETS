import logging
from typing import Annotated

from fastapi import APIRouter, Header, HTTPException

from app.chains.analyze import analyze
from app.schemas.analyze_request import AnalyzeRequest
from app.schemas.analyze_response import AnalyzeResponse
from app.schemas.error_response import ErrorResponse
from app.services.cv.get_cv import get_cv
from app.services.extensions.find_extension_id import find_extension_id
from app.services.extensions.record_extension_use import record_extension_use
from app.services.job_boards.is_job_url_allowed import is_job_url_allowed
from app.services.scans.find_previous_scan import find_previous_scan
from app.services.usage.record_scan import record_scan
from app.types.verified_user import VerifiedUser

logger = logging.getLogger(__name__)

router = APIRouter(
    tags=["analyze"],
    responses={
        401: {"model": ErrorResponse, "description": "Missing or invalid token."},
        403: {
            "model": ErrorResponse,
            "description": "Email not verified, extension removed, or job board not enabled.",
        },
        404: {"model": ErrorResponse, "description": "The user hasn't uploaded a CV yet."},
        422: {"description": "Invalid input: the job text is missing, too short, or too long."},
        502: {"model": ErrorResponse, "description": "The AI model or storage failed."},
        503: {"model": ErrorResponse, "description": "The service is unavailable."},
    },
)


@router.post(
    "/analyze",
    response_model=AnalyzeResponse,
    response_description="Verdict, score, and reasons for the match.",
    summary="Smash or pass a job post",
    description=(
        "Compares the logged-in user's stored CV with a job post. If this user already scanned "
        "the same page, the stored result is returned with already_scanned set to true, and "
        "nothing is counted again."
    ),
)
def analyze_job(
    payload: AnalyzeRequest,
    user: VerifiedUser,
    install_id: Annotated[str | None, Header(alias="X-ETS-Install-Id", max_length=64)] = None,
) -> AnalyzeResponse:

    cv = get_cv(user.id)
    if cv is None:
        raise HTTPException(status_code=404, detail="Upload your CV before scanning a job.")

    if install_id and find_extension_id(user.id, install_id) is None:
        raise HTTPException(
            status_code=403,
            detail="This extension was removed from your account. Log in again.",
        )

    if not is_job_url_allowed(user, payload.job_url):
        raise HTTPException(
            status_code=403,
            detail="This job board isn't enabled for your account. Check Settings, Job boards.",
        )

    previous = find_previous_scan(user.id, payload.job_url)
    if previous is not None:
        record_extension_use(user.id, install_id, counted=False)
        return AnalyzeResponse(**previous.model_dump(), already_scanned=True)

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

    record_scan(user, result, payload.job_url, payload.job_title, payload.job_text, install_id)
    return AnalyzeResponse(**result.model_dump())
