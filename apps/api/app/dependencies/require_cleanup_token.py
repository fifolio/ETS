import secrets
from typing import Annotated

from fastapi import Header, HTTPException

from app.core.config import settings


def require_cleanup_token(x_cleanup_token: Annotated[str | None, Header()] = None) -> None:
    if not settings.cleanup_token:
        raise HTTPException(status_code=503, detail="The cleanup is disabled.")
    if x_cleanup_token is None or not secrets.compare_digest(
        x_cleanup_token, settings.cleanup_token
    ):
        raise HTTPException(status_code=401, detail="Invalid cleanup token.")
