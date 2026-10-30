from pydantic import Field

from app.schemas.error_response import ErrorResponse


class CVValidationErrorResponse(ErrorResponse):
    problems: list[str] = Field(description="What is wrong with the CV, one message per problem")
