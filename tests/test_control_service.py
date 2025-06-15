import ast
import os
import subprocess
from types import SimpleNamespace, ModuleType
from unittest import mock

import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
aiohttp_mod = ModuleType('aiohttp')
aiohttp_mod.ClientSession = object
aiohttp_mod.ClientTimeout = lambda *a, **k: None
aiohttp_mod.ClientError = Exception
sys.modules['aiohttp'] = aiohttp_mod
from piwardrive import utils
from piwardrive import security
from typing import Any, Callable, cast


def _load_control_service() -> Callable[[Any, str, str], Any]:
    src = open(os.path.join(os.path.dirname(__file__), '..', 'src', 'piwardrive', 'main.py')).read()
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
    monkeypatch.setenv('PW_ADMIN_PASSWORD', 'x')
    func = _load_control_service()
    dummy = SimpleNamespace(
        _run_service_cmd=lambda *_a, **_k: (False, '', 'oops')
    )
    with mock.patch.object(utils, 'report_error') as rep:

        func(dummy, 'svc', 'start')
    rep.assert_called_once_with('Failed to start svc: oops')


def test_control_service_prompts_for_password(monkeypatch: Any) -> None:
    def fake_verify(pw: str, h: str) -> bool:
        calls.append((pw, h))
        return False

    calls: list[tuple[str, str]] = []
    monkeypatch.delenv('PW_ADMIN_PASSWORD', raising=False)
    monkeypatch.setattr(security, 'verify_password', fake_verify)
    prompts: list[str] = []
    monkeypatch.setattr('getpass.getpass', lambda prompt='': (prompts.append(prompt), 'pw')[1])

    func = _load_control_service()
    dummy = SimpleNamespace(
        _run_service_cmd=lambda *_a, **_k: (True, '', ''),
        config_data=SimpleNamespace(admin_password_hash='hash'),
    )
    with mock.patch.object(utils, 'report_error') as rep:
        func(dummy, 'svc', 'start')
    rep.assert_called_once_with('Unauthorized')
    assert prompts
    assert calls

