import importlib
import json
import sys
from types import SimpleNamespace

import pytest


@pytest.fixture(autouse=True)
def _stub_pydantic(monkeypatch):
    """Provide a minimal pydantic stub so config imports succeed."""
    module = SimpleNamespace(
        BaseModel=object,
        Field=lambda *a, **k: None,
        ValidationError=Exception,
    )
    module.field_validator = lambda *a, **k: (lambda f: f)
    monkeypatch.setitem(sys.modules, "pydantic", module)


def _import_cli():
    for name in ["piwardrive.cli.config_cli", "piwardrive.scripts.config_cli"]:
        if name in sys.modules:
            del sys.modules[name]
    return importlib.import_module("piwardrive.cli.config_cli")


def test_config_cli_get_local(monkeypatch, capsys):
    cli = _import_cli()
    monkeypatch.setattr(cli.cfg, "load_config", lambda: cli.cfg.Config(mysql_host="db"))
    cli.main(["get", "mysql_host"])
    assert capsys.readouterr().out.strip() == json.dumps("db")


def test_config_cli_set_local(monkeypatch, capsys):
    cli = _import_cli()
    cfg_obj = cli.cfg.Config(map_auto_prefetch=False)
    monkeypatch.setattr(cli.cfg, "load_config", lambda: cfg_obj)
    saved = {}

    def fake_save(c):
        saved["cfg"] = c

    monkeypatch.setattr(cli.cfg, "save_config", fake_save)
    cli.main(["set", "map_auto_prefetch", "true"])
    assert saved["cfg"].map_auto_prefetch is True
    assert capsys.readouterr().out.strip() == "true"


def test_config_cli_get_api(monkeypatch, capsys):
    cli = _import_cli()

    async def fake_get(url):
        assert url == "http://api"
        return {"mysql_host": "db"}

    monkeypatch.setattr(cli, "_api_get", fake_get)
    cli.main(["--url", "http://api", "get", "mysql_host"])
    assert capsys.readouterr().out.strip() == json.dumps("db")


def test_config_cli_set_api(monkeypatch, capsys):
    cli = _import_cli()

    async def fake_get(url):
        assert url == "http://api"
        return {"mysql_host": "db"}

    async def fake_update(url, updates):
        assert url == "http://api"
        assert updates == {"mysql_host": "new"}
        return {"mysql_host": "new"}

    monkeypatch.setattr(cli, "_api_get", fake_get)
    monkeypatch.setattr(cli, "_api_update", fake_update)
    cli.main(["--url", "http://api", "set", "mysql_host", "new"])
    assert capsys.readouterr().out.strip() == json.dumps("new")


def test_config_cli_get_unknown_local(monkeypatch):
    cli = _import_cli()
    monkeypatch.setattr(cli.cfg, "load_config", lambda: cli.cfg.Config())
    with pytest.raises(SystemExit):
        cli.main(["get", "does_not_exist"])


def test_config_cli_set_unknown_local(monkeypatch):
    cli = _import_cli()
    monkeypatch.setattr(cli.cfg, "load_config", lambda: cli.cfg.Config())
    with pytest.raises(SystemExit):
        cli.main(["set", "does_not_exist", "value"])


def test_config_cli_get_unknown_api(monkeypatch):
    cli = _import_cli()

    async def fake_get(url):
        assert url == "http://api"
        return {"mysql_host": "db"}

    monkeypatch.setattr(cli, "_api_get", fake_get)
    with pytest.raises(SystemExit):
        cli.main(["--url", "http://api", "get", "does_not_exist"])


def test_config_cli_set_unknown_api(monkeypatch):
    cli = _import_cli()

    async def fake_get(url):
        assert url == "http://api"
        return {"mysql_host": "db"}

    monkeypatch.setattr(cli, "_api_get", fake_get)
    with pytest.raises(SystemExit):
        cli.main(["--url", "http://api", "set", "does_not_exist", "1"])
