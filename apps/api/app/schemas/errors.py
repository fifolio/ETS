from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    detail: str = Field(
        description="A human-readable description of the error that occurred.",
    )


class CVValidationErrorResponse(ErrorResponse):
    problems: list[str] = Field(description="What is wrong with the CV, one message per problem")
