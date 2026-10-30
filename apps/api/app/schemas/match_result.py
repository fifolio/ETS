from pydantic import BaseModel, ConfigDict, Field

from app.schemas.verdict import Verdict


class MatchResult(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "verdict": "smash",
                    "score": 84,
                    "summary": (
                        "Strong fit: your React and TypeScript experience matches the core "
                        "requirements. Only testing experience is missing."
                    ),
                    "matching_skills": ["React", "TypeScript", "Tailwind CSS"],
                    "missing_skills": ["Vitest"],
                    "red_flags": [],
                }
            ]
        }
    )

    verdict: Verdict = Field(description="smash if the job is worth applying to, otherwise pass")
    score: int = Field(ge=0, le=100, description="How well the CV fits the job's real requirements")
    summary: str = Field(description="Two short sentences explaining the verdict")
    matching_skills: list[str] = Field(description="Skills the CV has that the job needs")
    missing_skills: list[str] = Field(description="Important requirements the CV lacks")
    red_flags: list[str] = Field(description="Unrealistic or suspicious things in the job post")
