import logging
from unittest import mock

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import report_error
from typing import Any


def test_report_error_logs_and_alerts(caplog: Any) -> None:
    app = mock.Mock()
    with mock.patch('utils.App.get_running_app', return_value=app):
        with caplog.at_level(logging.ERROR):
            report_error("boom")
    assert app.show_alert.call_count == 1
    assert "boom" in caplog.text
