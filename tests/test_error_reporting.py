import logging
from typing import Any

from piwardrive.utils import report_error


def test_report_error_logs(caplog: Any) -> None:
    with caplog.at_level(logging.ERROR):
        report_error("boom")
    assert "boom" in caplog.text
