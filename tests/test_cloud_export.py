import logging
import subprocess
from typing import Any

import pytest

from piwardrive import cloud_export


def test_upload_to_s3_logs_errors(monkeypatch: Any, caplog: Any) -> None:
    monkeypatch.setattr(cloud_export.os.path, "exists", lambda p: True)

    def fake_run(*args: Any, **kwargs: Any) -> None:
        raise subprocess.CalledProcessError(1, args[0])

    monkeypatch.setattr(cloud_export.subprocess, "run", fake_run)

    with caplog.at_level(logging.ERROR):
        with pytest.raises(subprocess.CalledProcessError):
            cloud_export.upload_to_s3("file", "bucket", "key")

    assert "S3 upload failed" in caplog.text
