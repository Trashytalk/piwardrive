from __future__ import annotations

import os

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from piwardrive.database_service import db_service
from piwardrive.persistence import User
from piwardrive.security import hash_secret

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
SECURITY_DEP = Depends(oauth2_scheme)


async def ensure_default_user() -> None:
    """Create default user account from environment variables if needed."""
    pw_hash = os.getenv("PW_API_PASSWORD_HASH")
    if not pw_hash:
        return
    username = os.getenv("PW_API_USER", "admin")
    if await db_service.get_user(username) is None:
        await db_service.save_user(User(username=username, password_hash=pw_hash))


async def check_auth(token: str = SECURITY_DEP) -> None:
    """Validate bearer token against stored users."""
    await ensure_default_user()
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    user = await db_service.get_user_by_token(hash_secret(token))
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")


AUTH_DEP = check_auth
