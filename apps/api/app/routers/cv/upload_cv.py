from fastapi import APIRouter, HTTPException, UploadFile

from app.constants.cv_parsing import MAX_CV_BYTES
from app.exceptions.cv_parsing_error import CVParsingError
from app.exceptions.cv_validation_error import CVValidationError
from app.routers.cv.options import CV_ROUTER_OPTIONS
from app.schemas.cv_info import CVInfo
from app.schemas.cv_validation_error_response import CVValidationErrorResponse
from app.schemas.error_response import ErrorResponse
from app.services.cv.save_cv import save_cv
from app.services.cv_parsing.extract_text_from_pdf import extract_text_from_pdf
from app.services.cv_validation.validate_cv import validate_cv
from app.types.current_user import CurrentUser

router = APIRouter(**CV_ROUTER_OPTIONS)


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
