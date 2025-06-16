import os
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest import mock
import builtins

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import r_integration


class DummyResult(list):
    def __init__(self, values, names):
        super().__init__(values)
        self.names = names


def test_health_summary_missing_rpy2():
    orig_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name.startswith("rpy2"):
            raise ImportError("No module named rpy2")
        return orig_import(name, *args, **kwargs)

    with mock.patch.dict(sys.modules, {"rpy2": None, "rpy2.robjects": None}):
        with mock.patch("builtins.__import__", side_effect=fake_import):
            with pytest.raises(RuntimeError, match="rpy2 is required"):
                r_integration.health_summary("file.csv")


def test_health_summary_no_plot():
    dummy_result = DummyResult([3], ["x"])
    r_source = mock.Mock()
    health_func = mock.Mock(return_value=dummy_result)
    robjects = SimpleNamespace(
        r=SimpleNamespace(source=r_source),
        globalenv={"health_summary": health_func},
        NULL="NULL",
    )
    with mock.patch.dict(
        sys.modules,
        {"rpy2": SimpleNamespace(robjects=robjects), "rpy2.robjects": robjects},
    ):
        result = r_integration.health_summary("data.csv")
    r_source.assert_called_once_with(
        str(Path(r_integration.__file__).parent / "scripts" / "health_summary.R")
    )
    health_func.assert_called_once_with("data.csv", "NULL")
    assert result == {"x": 3.0}


def test_health_summary_with_plot():
    dummy_result = DummyResult([1, 2], ["a", "b"])
    r_source = mock.Mock()
    health_func = mock.Mock(return_value=dummy_result)
    robjects = SimpleNamespace(
        r=SimpleNamespace(source=r_source),
        globalenv={"health_summary": health_func},
        NULL="NULL",
    )
    with mock.patch.dict(
        sys.modules,
        {"rpy2": SimpleNamespace(robjects=robjects), "rpy2.robjects": robjects},
    ):
        result = r_integration.health_summary("data.csv", plot_path="out.png")
    r_source.assert_called_once_with(
        str(Path(r_integration.__file__).parent / "scripts" / "health_summary.R")
    )
    health_func.assert_called_once_with("data.csv", "out.png")
    assert result == {"a": 1.0, "b": 2.0}
