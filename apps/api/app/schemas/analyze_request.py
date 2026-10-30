from pydantic import BaseModel, ConfigDict, Field


class AnalyzeRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "job_text": (
                        "Frontend Developer (React). We are looking for a developer to build "
                        "and maintain our web app with React and TypeScript. 1-3 years of "
                        "experience. Nice to have: Tailwind CSS, testing with Vitest."
                    ),
                    "job_url": "https://example.com/jobs/frontend-developer",
                    "job_title": "Frontend Developer",
                }
            ]
        }
    )

    job_text: str = Field(
        min_length=50,
        max_length=50_000,
        description="Text of the job post, as scraped from the page",
    )
    job_url: str | None = Field(default=None, max_length=2000, description="Page URL")
    job_title: str | None = Field(default=None, max_length=255, description="Job title")
