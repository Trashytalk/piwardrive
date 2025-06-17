"""Export helpers for uploading files to cloud storage."""

from __future__ import annotations

import logging
import os
import subprocess
from typing import Optional

logger = logging.getLogger(__name__)


def upload_to_s3(
    file_path: str, bucket: str, key: str, profile: Optional[str] = None
) -> None:
    """Upload ``file_path`` to the given S3 ``bucket`` using the AWS CLI."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(file_path)
    cmd = ["aws", "s3", "cp", file_path, f"s3://{bucket}/{key}"]
    if profile:
        cmd.extend(["--profile", profile])
    try:
        subprocess.run(cmd, check=True)
        logger.info("Uploaded %s to s3://%s/%s", file_path, bucket, key)
    except Exception as exc:  # pragma: no cover - runtime errors
        logger.error("S3 upload failed: %s", exc)
        raise
