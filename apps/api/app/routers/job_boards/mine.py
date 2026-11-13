from fastapi import APIRouter

from app.schemas.error_response import ErrorResponse
from app.schemas.my_job_boards import MyJobBoards
from app.services.job_boards.get_user_job_boards import get_user_job_boards
from app.services.job_boards.to_job_board_out import to_job_board_out
from app.types.verified_user import VerifiedUser

router = APIRouter(
    prefix="/job-boards",
    tags=["job-boards"],
    responses={
        401: {"model": ErrorResponse, "description": "Missing or invalid token."},
        403: {"model": ErrorResponse, "description": "The user's email isn't verified yet."},
        502: {"model": ErrorResponse, "description": "The storage service failed."},
    },
)


@router.get(
    "/mine",
    response_model=MyJobBoards,
    summary="The job boards active for the logged-in user",
    description=(
        "The boards included in the user's plan. The extension reads a page only when its "
        "address is under one of these boards."
    ),
)
def my_job_boards(user: VerifiedUser) -> MyJobBoards:
    result = get_user_job_boards(user)
    return MyJobBoards(
        boards=[to_job_board_out(board) for board in result.boards], plan=result.plan
    )
