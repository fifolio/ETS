from app.services.job_boards.url_matches_board import url_matches_board
from app.types.job_board import JobBoard


def find_covering_board(url: str, boards: list[JobBoard]) -> JobBoard | None:
    """A supported board that already covers this address, or sits inside a broader one."""
    for board in boards:
        if url_matches_board(url, board.url) or url_matches_board(board.url, url):
            return board
    return None
