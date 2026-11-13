import time
from typing import Any

from app.constants.job_boards import JOB_BOARDS_CACHE_SECONDS
from app.services.job_boards.fetch_job_boards import fetch_job_boards
from app.types.job_board import JobBoard

_cache: dict[str, Any] = {"value": None, "expires_at": 0.0}


def list_active_job_boards() -> list[JobBoard]:
    """The active job boards, read from the table at most once a minute."""
    now = time.monotonic()
    cached = _cache["value"]
    if cached is not None and now < _cache["expires_at"]:
        return list(cached)
    boards = fetch_job_boards()
    _cache["value"] = boards
    _cache["expires_at"] = now + JOB_BOARDS_CACHE_SECONDS
    return list(boards)
