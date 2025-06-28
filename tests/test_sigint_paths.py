import importlib
import os


def test_export_dir_env_override(monkeypatch, tmp_path):
    monkeypatch.setenv("EXPORT_DIR", str(tmp_path))
    import piwardrive.sigint_suite.paths as p

    importlib.reload(p)
    assert p.EXPORT_DIR == str(tmp_path)
