import logging

from appwrite.exception import AppwriteException
from fastapi import Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


async def appwrite_error_handler(request: Request, exc: AppwriteException) -> JSONResponse:
    logger.error("Appwrite error %s: %s", exc.code, exc.message)
    return JSONResponse(
        status_code=502,
        content={"detail": "The storage service failed. Please try again."},
    )
