"""Export helpers for uploading files to cloud storage."""

from __future__ import annotations

import logging
import os
from typing import Any, Optional

import boto3

logger = logging.getLogger(__name__)


def upload_to_s3(
    file_path: str,
    bucket: str,
    key: str,
    profile: Optional[str] = None,
    extra_args: Optional[dict[str, Any]] = None,
) -> None:
    """Upload ``file_path`` to the given S3 ``bucket`` using :mod:`boto3`."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(file_path)

    session = boto3.Session(profile_name=profile) if profile else boto3.Session()
    s3 = session.client("s3")

    try:
        s3.upload_file(file_path, bucket, key, ExtraArgs=extra_args or {})
        logger.info("Uploaded %s to s3://%s/%s", file_path, bucket, key)
    except Exception as exc:  # pragma: no cover - runtime errors
        logger.error("S3 upload failed: %s", exc)
        raise
