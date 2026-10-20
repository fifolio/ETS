from enum import StrEnum

from pydantic import BaseModel, Field


class Verdict(StrEnum):
    SMASH = "smash"
    PASS = "pass"

class MatchResult(BaseModel):
    verdict: Verdict = Field(description="smash if the job is worth applying to, otherwise pass", )
    score: int = Field(ge=0, le=100, description="How well the CV fits the job's real requirements")
    summary: str = Field(description="Two short sentences explaining the verdict")
    matching_skills: list[str] = Field(description="Skills the CV has that the job needs")
    missing_skills: list[str] = Field(description="Skills the job needs that the CV doesn't have")
    red_flags: list[str] = Field(description="Red flags that make the CV a bad fit for the job")