from __future__ import annotations

"""Authentication API routes."""

import secrets

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from piwardrive.database_service import db_service
from piwardrive.security import hash_secret, verify_password
from piwardrive.exceptions import ServiceError

from .dependencies import AUTH_DEP, SECURITY_DEP, ensure_default_user
from ..health.models import TokenResponse, AuthLoginResponse, LogoutResponse  # types shared

router = APIRouter()


@router.post("/token")
async def token_login(form: OAuth2PasswordRequestForm = Depends()) -> TokenResponse:
    """Return bearer token for valid credentials."""
    await ensure_default_user()
    user = await db_service.get_user(form.username)
    if not user or not verify_password(form.password, user.password_hash):
        raise ServiceError("Unauthorized", status_code=401)
    token = secrets.token_urlsafe(32)
    await db_service.update_user_token(user.username, hash_secret(token))
    return {"access_token": token, "token_type": "bearer"}


@router.post("/auth/login")
async def login(form: OAuth2PasswordRequestForm = Depends()) -> AuthLoginResponse:
    """Validate credentials and return a bearer token."""
    user = await db_service.get_user(form.username)
    if not user or not verify_password(form.password, user.password_hash):
        raise ServiceError("Unauthorized", status_code=401)
    token = secrets.token_urlsafe(32)
    TOKENS[token] = user.username
    return {"access_token": token, "token_type": "bearer", "role": user.role}


@router.post("/auth/logout")
async def logout(token: str = SECURITY_DEP) -> LogoutResponse:
    """Invalidate the provided token."""
    TOKENS.pop(token, None)
    return {"logout": True}

# in-memory token store retained for compatibility
TOKENS: dict[str, str] = {}
