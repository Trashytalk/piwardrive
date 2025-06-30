import logging
from typing import Any

import pytest

from piwardrive import cloud_export


def test_upload_to_s3_logs_errors(monkeypatch: Any, caplog: Any) -> None:
    monkeypatch.setattr(cloud_export.os.path, "exists", lambda p: True)

    class DummyClient:
        def upload_file(self, *args: Any, **kwargs: Any) -> None:
            raise RuntimeError("boom")

    class DummySession:
        def __init__(self, profile_name: str | None = None) -> None:
            pass

        def client(self, name: str) -> DummyClient:
            assert name == "s3"
            return DummyClient()

    monkeypatch.setattr(cloud_export.boto3, "Session", DummySession)

    with caplog.at_level(logging.ERROR):
        with pytest.raises(RuntimeError):
            cloud_export.upload_to_s3("file", "bucket", "key")

    assert "S3 upload failed" in caplog.text
