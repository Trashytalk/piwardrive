import importlib.util
import os
import sys
from types import SimpleNamespace
from unittest import mock

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import r_integration

if importlib.util.find_spec("rpy2") is None:
    pytest.skip("rpy2 is not installed", allow_module_level=True)


class DummyResult(list):
    def __init__(self, values, names):
        super().__init__(values)
        self.names = names


def test_health_summary_mocked() -> None:
    dummy_result = DummyResult([1, 2], ["a", "b"])
    robjects = SimpleNamespace(
        r=SimpleNamespace(source=lambda _path: None),
        globalenv={"health_summary": lambda path, plot: dummy_result},
        NULL=None,
    )
    with mock.patch("rpy2.robjects", robjects):
        result = r_integration.health_summary("data.csv", plot_path="plot.png")
    assert result == {"a": 1.0, "b": 2.0}
