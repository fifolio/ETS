from pydantic import BaseModel, ConfigDict, Field


class AnalyzeRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "cv_text": (
                        "Jane Doe. Junior frontend developer with 2 years of experience "
                        "building web apps with React, TypeScript, and Tailwind CSS. "
                        "Built and shipped a job board and a dashboard used by 500 students."
                    ),
                    "job_text": (
                        "Frontend Developer (React). We are looking for a developer to build "
                        "and maintain our web app with React and TypeScript. 1-3 years of "
                        "experience. Nice to have: Tailwind CSS, testing with Vitest."
                    ),
                }
            ]
        }
    )

    cv_text: str = Field(
        min_length=100,
        max_length=20_000,
        description="Plain text of the candidate's CV",
    )
    job_text: str = Field(
        min_length=50,
        max_length=50_000,
        description="Text of the job post, as scraped from the page",
    )
