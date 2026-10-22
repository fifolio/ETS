from fastapi import APIRouter, HTTPException, UploadFile

from app.core.auth import CurrentUserId
from app.schemas.cv import CVInfo
from app.schemas.errors import ErrorResponse
from app.services.cv_parser import CVParsingError, extract_text_from_pdf
from app.services.cv_store import get_cv, save_cv

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
    description="Upload a PDF CV. The text is extracted and saved, replacing any previous CV.",
    responses={
        413: {"model": ErrorResponse, "description": "File is larger than 5 MB."},
        422: {"model": ErrorResponse, "description": "The file can't be read as a CV."},
    },
)
def upload_cv(user_id: CurrentUserId, file: UploadFile) -> CVInfo:
    data = file.file.read(MAX_CV_BYTES + 1)
    if len(data) > MAX_CV_BYTES:
        raise HTTPException(status_code=413, detail="The CV file is larger than 5 MB.")
    try:
        text = extract_text_from_pdf(data)
    except CVParsingError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    file_name = file.filename or "cv.pdf"
    save_cv(user_id, file_name, data, text)
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
