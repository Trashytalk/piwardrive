"""JWT token utilities for authentication.

This module provides functions for creating and verifying JWT tokens
used in PiWardrive authentication. It supports both access tokens
and refresh tokens with configurable expiration times.
"""

import os
import time
from typing import Optional

import jwt

SECRET = os.getenv("PW_JWT_SECRET", "change-me")
ALGORITHM = os.getenv("PW_JWT_ALG", "HS256")
ACCESS_EXPIRE = int(os.getenv("PW_JWT_EXPIRE", "3600"))
REFRESH_EXPIRE = int(os.getenv("PW_JWT_REFRESH", "86400"))


def create_access_token(username: str, expires_in: int = ACCESS_EXPIRE) -> str:
    """Create a JWT access token for a user.
    
    Args:
        username: Username to encode in the token.
        expires_in: Token expiration time in seconds.
        
    Returns:
        Encoded JWT access token string.
    """
    payload = {"sub": username, "exp": int(time.time()) + expires_in}
    return jwt.encode(payload, SECRET, algorithm=ALGORITHM)


def create_refresh_token(username: str, expires_in: int = REFRESH_EXPIRE) -> str:
    """Create a JWT refresh token for a user.
    
    Args:
        username: Username to encode in the token.
        expires_in: Token expiration time in seconds.
        
    Returns:
        Encoded JWT refresh token string.
    """
    payload = {
        "sub": username,
        "type": "refresh",
        "exp": int(time.time()) + expires_in,
    }
    return jwt.encode(payload, SECRET, algorithm=ALGORITHM)


def verify_token(token: str) -> Optional[str]:
    """Verify a JWT token and extract the username.
    
    Args:
        token: JWT token string to verify.
        
    Returns:
        Username from the token if valid, None if invalid or expired.
    """
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        return None
    return payload.get("sub")
