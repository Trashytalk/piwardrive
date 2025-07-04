from __future__ import annotations

"""Authentication API routes."""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from piwardrive import service
from piwardrive.database_service import db_service
from piwardrive.persistence import User
from piwardrive.security import hash_secret, verify_password

router = APIRouter()

async def _ensure_default_user() -> None:
    pw_hash = service.os.getenv("PW_API_PASSWORD_HASH")
    if not pw_hash:
        return
    username = service.os.getenv("PW_API_USER", "admin")
    if await db_service.get_user(username) is None:
        await db_service.save_user(User(username=username, password_hash=pw_hash))

async def _check_auth(token: str = service.SECURITY_DEP) -> None:
    await _ensure_default_user()
    if not token:
        raise HTTPException(status_code=401, detail=service.error_json(401, "Unauthorized"))
    user = await db_service.get_user_by_token(hash_secret(token))
    if user is None:
        raise HTTPException(status_code=401, detail=service.error_json(401, "Unauthorized"))

AUTH_DEP = Depends(_check_auth)

@router.post("/token")
async def token_login(form: OAuth2PasswordRequestForm = Depends()) -> service.TokenResponse:
    await _ensure_default_user()
    user = await db_service.get_user(form.username)
    if not user or not verify_password(form.password, user.password_hash):
        raise HTTPException(status_code=401, detail=service.error_json(401, "Unauthorized"))
    token = service.secrets.token_urlsafe(32)
    await db_service.update_user_token(user.username, hash_secret(token))
    return {"access_token": token, "token_type": "bearer"}

@router.post("/auth/login")
async def login(form: OAuth2PasswordRequestForm = Depends()) -> service.AuthLoginResponse:
    user = await db_service.get_user(form.username)
    if not user or not verify_password(form.password, user.password_hash):
        raise HTTPException(status_code=401, detail=service.error_json(401, "Unauthorized"))
    token = service.secrets.token_urlsafe(32)
    service.TOKENS[token] = user.username
    return {"access_token": token, "token_type": "bearer", "role": user.role}

@router.post("/auth/logout")
async def logout(token: str = service.SECURITY_DEP) -> service.LogoutResponse:
    service.TOKENS.pop(token, None)
    return {"logout": True}
