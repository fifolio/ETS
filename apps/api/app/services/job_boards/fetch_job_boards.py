from app.core.config import settings
from app.schemas.job_board_row import JobBoardRow
from app.services.appwrite.iter_table_rows import iter_table_rows
from app.services.job_boards.normalize_min_plan import normalize_min_plan
from app.types.job_board import JobBoard


def fetch_job_boards() -> list[JobBoard]:
    """The active job boards from the table, sorted by name."""
    rows = iter_table_rows(settings.appwrite_job_boards_table_id, JobBoardRow)
    boards = [
        JobBoard(
            id=row.id,
            name=row.data.name,
            url=row.data.url,
            min_plan=normalize_min_plan(row.data.minPlan),
        )
        for row in rows
        if row.data.isActive
    ]
    return sorted(boards, key=lambda board: board.name.lower())
