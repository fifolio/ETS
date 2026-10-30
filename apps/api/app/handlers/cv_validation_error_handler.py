from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions.cv_validation_error import CVValidationError


async def cv_validation_error_handler(request: Request, exc: CVValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={"detail": "The CV did not pass validation.", "problems": exc.problems},
    )
