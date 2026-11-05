from fastapi import APIRouter, HTTPException

from app.routers.cv.options import CV_ROUTER_OPTIONS
from app.schemas.error_response import ErrorResponse
from app.services.cv.delete_cv import delete_cv
from app.types.verified_user import VerifiedUserId

router = APIRouter(**CV_ROUTER_OPTIONS)


@router.delete(
    "",
    status_code=204,
    summary="Delete your CV",
    responses={404: {"model": ErrorResponse, "description": "No CV uploaded yet."}},
)
def remove_cv(user_id: VerifiedUserId) -> None:
    if not delete_cv(user_id):
        raise HTTPException(status_code=404, detail="No CV uploaded yet.")
