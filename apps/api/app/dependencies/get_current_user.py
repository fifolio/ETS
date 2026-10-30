from typing import Annotated

from appwrite.exception import AppwriteException
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from app.dependencies.bearer_scheme import bearer_scheme
from app.services.appwrite.verify_jwt import verify_jwt
from app.types.authenticated_user import AuthenticatedUser


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
) -> AuthenticatedUser:
    unauthorized = HTTPException(
        status_code=401,
        detail="Invalid or missing token.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if credentials is None:
        raise unauthorized
    try:
        return verify_jwt(credentials.credentials)
    except AppwriteException as exc:
        if exc.code == 401:
            raise unauthorized from exc
        raise  # Appwrite itself is failing, so let the 502 handler deal with it
