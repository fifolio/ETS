import logging

from appwrite.exception import AppwriteException
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__file__)


class ConfigurationError(RuntimeError):
    """Raised when required settings, like Appwrite credentials, are missing."""


def register_exception_handlers(app: FastAPI) -> None:
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
