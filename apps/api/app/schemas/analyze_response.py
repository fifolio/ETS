from pydantic import Field

from app.schemas.match_result import MatchResult


class AnalyzeResponse(MatchResult):
    already_scanned: bool = Field(
        default=False,
        description="True when this page was scanned before: the stored result is returned",
    )
