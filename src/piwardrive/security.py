"""Security utilities for input validation and encryption."""

import base64
import binascii
import hashlib
import os
import re
import secrets

import bcrypt
from cryptography.fernet import Fernet

_ALLOWED_SERVICE_RE: re.Pattern[str] = re.compile(r"^[\w.-]+$")
_ALLOWED_FILENAME_RE: re.Pattern[str] = re.compile(r"^[\w.-]+$")


def sanitize_path(path: str) -> str:
    """Return a normalized path without unsafe segments."""
    normalized = os.path.normpath(path)
    if ".." in normalized.split(os.sep):
        raise ValueError(f"Unsafe path: {path}")
    return normalized


def validate_service_name(name: str) -> None:
    """Raise ``ValueError`` if ``name`` contains unsafe characters."""
    if not _ALLOWED_SERVICE_RE.fullmatch(name):
        raise ValueError(f"Invalid service name: {name}")


def validate_filename(name: str) -> None:
    """Raise ``ValueError`` if ``name`` contains unsafe characters."""
    if not _ALLOWED_FILENAME_RE.fullmatch(name):
        raise ValueError(f"Invalid filename: {name}")


def sanitize_filename(filename: str) -> str:
    """Return ``filename`` sanitized for safe storage."""
    name = os.path.basename(filename)
    if name != filename:
        raise ValueError(f"Invalid filename: {filename}")
    validate_filename(name)
    return name


def hash_password(password: str) -> str:
    """Return a bcrypt hash of ``password``."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    """Return ``True`` if ``password`` matches ``hashed``. Supports legacy PBKDF2 hashes."""
    if hashed.startswith("$2"):
        try:
            return bcrypt.checkpw(password.encode(), hashed.encode())
        except ValueError:
            return False
    try:
        data = base64.b64decode(hashed)
        salt, digest = data[:16], data[16:]
        check = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100_000)
        return secrets.compare_digest(check, digest)
    except (binascii.Error, ValueError):
        return False


def encrypt_data(data: str, key: bytes) -> str:
    """Encrypt ``data`` with ``key``."""
    return Fernet(key).encrypt(data.encode()).decode()


def decrypt_data(token: str, key: bytes) -> str:
    """Decrypt ``token`` with ``key``."""
    return Fernet(key).decrypt(token.encode()).decode()


def hash_secret(secret: str) -> str:
    """Return a SHA256 hex digest of ``secret``."""
    return hashlib.sha256(secret.encode()).hexdigest()
