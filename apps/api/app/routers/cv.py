from fastapi import APIRouter, HTTPException, UploadFile

from app.core.auth import CurrentUser, CurrentUserId
from app.core.errors import CVValidationError
from app.schemas.cv import CVInfo
from app.schemas.errors import CVValidationErrorResponse, ErrorResponse
from app.services.cv_parser import CVParsingError, extract_text_from_pdf
from app.services.cv_store import get_cv, save_cv
from app.services.cv_validator import validate_cv

MAX_CV_BYTES = 5 * 1024 * 1024  # matches the Appwrite bucket limit

router = APIRouter(
    prefix="/cv",
    tags=["cv"],
    responses={
        401: {"model": ErrorResponse, "description": "Missing or invalid token."},
        502: {"model": ErrorResponse, "description": "The storage service failed."},
        503: {"model": ErrorResponse, "description": "The service is not configured."},
    },
)


@router.post(
    "",
    response_model=CVInfo,
    status_code=201,
    summary="Upload your CV",
    description=(
        "Upload a PDF CV. It must contain your account name and email and at least one "
        "Education, Experience, Skills, or Profile section. The text is extracted and saved, "
        "replacing any previous CV."
    ),
    responses={
        413: {"model": ErrorResponse, "description": "File is larger than 5 MB."},
        422: {
            "model": CVValidationErrorResponse,
            "description": "The file isn't a readable PDF, or the CV didn't pass validation.",
        },
    },
)
def upload_cv(user: CurrentUser, file: UploadFile) -> CVInfo:
    data = file.file.read(MAX_CV_BYTES + 1)
    if len(data) > MAX_CV_BYTES:
        raise HTTPException(status_code=413, detail="The CV file is larger than 5 MB.")

    try:
        text = extract_text_from_pdf(data)
    except CVParsingError as exc:
        raise CVValidationError([str(exc)]) from exc

    problems = validate_cv(text, account_name=user.name, account_email=user.email)
    if problems:
        raise CVValidationError(problems)

    file_name = file.filename or "cv.pdf"
    save_cv(user.id, file_name, data, text)
    return CVInfo(file_name=file_name, characters=len(text))


@router.get(
    "",
    response_model=CVInfo,
    summary="Get your stored CV info",
    responses={404: {"model": ErrorResponse, "description": "No CV uploaded yet."}},
)
def read_cv(user_id: CurrentUserId) -> CVInfo:
    cv = get_cv(user_id)
    if cv is None:
        raise HTTPException(status_code=404, detail="No CV uploaded yet.")
    return CVInfo(file_name=cv.file_name, characters=len(cv.text))
