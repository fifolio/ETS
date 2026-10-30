from fastapi import APIRouter, HTTPException

from app.routers.cv.options import CV_ROUTER_OPTIONS
from app.schemas.cv_info import CVInfo
from app.schemas.error_response import ErrorResponse
from app.services.cv.get_cv import get_cv
from app.types.current_user import CurrentUserId

router = APIRouter(**CV_ROUTER_OPTIONS)


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
