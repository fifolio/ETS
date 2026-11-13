from app.services.job_boards.get_user_job_boards import get_user_job_boards
from app.services.job_boards.url_matches_board import url_matches_board
from app.types.authenticated_user import AuthenticatedUser


def is_job_url_allowed(user: AuthenticatedUser, job_url: str) -> bool:
    """True when the page is under one of the user's active job boards."""
    boards = get_user_job_boards(user).boards
    return any(url_matches_board(job_url, board.url) for board in boards)
