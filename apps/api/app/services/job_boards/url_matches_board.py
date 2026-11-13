from urllib.parse import urlsplit


def url_matches_board(page_url: str, board_url: str) -> bool:
    """True when the page is on the board's host and at or below the board's path."""
    try:
        page = urlsplit(page_url.strip())
        board = urlsplit(board_url.strip())
        page_host = (page.hostname or "").removeprefix("www.")
        board_host = (board.hostname or "").removeprefix("www.")
    except ValueError:
        return False
    if page.scheme not in ("http", "https") or board.scheme not in ("http", "https"):
        return False
    if not page_host or page_host != board_host:
        return False
    board_path = board.path.rstrip("/").lower()
    page_path = page.path.lower()
    return board_path == "" or page_path == board_path or page_path.startswith(f"{board_path}/")
