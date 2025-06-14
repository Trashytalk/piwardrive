import ast
import os
import subprocess
from types import SimpleNamespace
from unittest import mock

import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import utils
from typing import Any, Callable, cast


def _load_control_service() -> Callable[[Any, str, str], Any]:
    src = open(os.path.join(os.path.dirname(__file__), '..', 'main.py')).read()
    mod = ast.parse(src)
    func_node = None
    for node in mod.body:
        if isinstance(node, ast.ClassDef) and node.name == 'PiWardriveApp':
            for item in node.body:
                if isinstance(item, ast.FunctionDef) and item.name == 'control_service':
                    func_node = item
                    break
    assert func_node is not None
    mod = ast.Module(body=[func_node], type_ignores=[])
    namespace = {'subprocess': subprocess, 'utils': utils}
    exec(compile(mod, '<control_service>', 'exec'), namespace)
    return cast(Callable[[Any, str, str], Any], namespace['control_service'])


def test_control_service_reports_error(monkeypatch: Any) -> None:
    func = _load_control_service()
    proc = SimpleNamespace(returncode=1, stderr='oops')
    monkeypatch.setattr(subprocess, 'run', lambda *a, **kw: proc)
    with mock.patch.object(utils, 'report_error') as rep:
        func(object(), 'svc', 'start')
    rep.assert_called_once_with('Failed to start svc: oops')
