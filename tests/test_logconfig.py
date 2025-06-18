import json
import logging
import os
import sys
import io

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from piwardrive.logconfig import setup_logging
from typing import Any


def test_setup_logging_writes_json(tmp_path: Any) -> None:
    log_file = tmp_path / "test.log"
    setup_logging(log_file=str(log_file), level=logging.INFO)
    logging.info("hello")
    with open(log_file) as f:
        data = json.loads(f.readline())
    assert data["message"] == "hello"
    assert data["level"] == "INFO"


def test_setup_logging_respects_env(monkeypatch: Any, tmp_path: Any) -> None:
    log_file = tmp_path / "env.log"
    monkeypatch.setenv("PW_LOG_LEVEL", "DEBUG")
    logger = setup_logging(log_file=str(log_file))
    logging.debug("hi")
    with open(log_file) as f:
        data = json.loads(f.readline())
    assert data["level"] == "DEBUG"
    assert logger.level == logging.DEBUG
    monkeypatch.delenv("PW_LOG_LEVEL")


def test_setup_logging_stdout(monkeypatch: Any, tmp_path: Any) -> None:
    log_file = tmp_path / "out.log"
    stream = io.StringIO()
    monkeypatch.setattr(sys, "stdout", stream)
    setup_logging(log_file=str(log_file), stdout=True)
    logging.warning("stream me")
    with open(log_file) as f:
        data = json.loads(f.readline())
    stdout_data = json.loads(stream.getvalue())
    assert data["message"] == "stream me"
    assert stdout_data["message"] == "stream me"
