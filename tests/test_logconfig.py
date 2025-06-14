import json
import logging
import os

from logconfig import setup_logging


def test_setup_logging_writes_json(tmp_path):
    log_file = tmp_path / "test.log"
    setup_logging(log_file=str(log_file), level=logging.INFO)
    logging.info("hello")
    with open(log_file) as f:
        data = json.loads(f.readline())
    assert data["message"] == "hello"
    assert data["level"] == "INFO"
