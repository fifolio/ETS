import logging

from appwrite.exception import AppwriteException
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__file__)


class ConfigurationError(RuntimeError):
    """Raised when required settings, like Appwrite credentials, are missing."""


class CVValidationError(Exception):
    """Raised when an uploaded CV can't be accepted. Carries one message per problem."""

    def __init__(self, problems: list[str]):
        super().__init__("; ".join(problems))
        self.problems = problems


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(CVValidationError)
    async def cv_validation_error_handler(request: Request, exc: CVValidationError):
        return JSONResponse(
            status_code=422,
            content={"detail": "The CV did not pass validation.", "problems": exc.problems},
        )

    @app.exception_handler(ConfigurationError)
    async def configuration_error_handler(request: Request, exc: ConfigurationError):
        logger.error("Configuration error: %s", exc)
        return JSONResponse(status_code=503, content={"detail": "The service is not configured."})

    @app.exception_handler(AppwriteException)
    async def appwrite_error_handler(request: Request, exc: AppwriteException):
        logger.error("Appwrite error %s: %s", exc.code, exc.message)
        return JSONResponse(
            status_code=502, content={"detail": "The storage service failed. Please try again."}
        )
