from pydantic import BaseModel, Field

from app.schemas.job_board_out import JobBoardOut


class MyJobBoards(BaseModel):
    boards: list[JobBoardOut] = Field(description="The job boards included in this user's plan")
    plan: str
