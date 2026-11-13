from fastapi import APIRouter, Response

from app.schemas.job_board_out import JobBoardOut
from app.services.job_boards.list_active_job_boards import list_active_job_boards
from app.services.job_boards.to_job_board_out import to_job_board_out

router = APIRouter(tags=["job-boards"])


@router.get(
    "/job-boards",
    response_model=list[JobBoardOut],
    summary="Every job board ETS supports",
    description="Public. The full list, before any plan limit.",
)
def job_boards(response: Response) -> list[JobBoardOut]:
    response.headers["Cache-Control"] = "public, max-age=60"
    return [to_job_board_out(board) for board in list_active_job_boards()]
