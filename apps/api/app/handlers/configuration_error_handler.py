import logging

from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions.configuration_error import ConfigurationError

logger = logging.getLogger(__name__)


async def configuration_error_handler(request: Request, exc: ConfigurationError) -> JSONResponse:
    logger.error("Configuration error: %s", exc)
    return JSONResponse(status_code=503, content={"detail": "The service is not configured."})
