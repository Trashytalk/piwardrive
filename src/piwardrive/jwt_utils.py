import os
import time
from typing import Optional

import jwt

SECRET = os.getenv("PW_JWT_SECRET", "change-me")
ALGORITHM = os.getenv("PW_JWT_ALG", "HS256")
ACCESS_EXPIRE = int(os.getenv("PW_JWT_EXPIRE", "3600"))
REFRESH_EXPIRE = int(os.getenv("PW_JWT_REFRESH", "86400"))


def create_access_token(username: str, expires_in: int = ACCESS_EXPIRE) -> str:
    payload = {"sub": username, "exp": int(time.time()) + expires_in}
    return jwt.encode(payload, SECRET, algorithm=ALGORITHM)


def create_refresh_token(username: str, expires_in: int = REFRESH_EXPIRE) -> str:
    payload = {
        "sub": username,
        "type": "refresh",
        "exp": int(time.time()) + expires_in,
    }
    return jwt.encode(payload, SECRET, algorithm=ALGORITHM)


def verify_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        return None
    return payload.get("sub")
