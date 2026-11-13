from dataclasses import dataclass

from app.types.job_board import JobBoard


@dataclass(frozen=True)
class UserJobBoards:
    boards: list[JobBoard]
    plan: str
