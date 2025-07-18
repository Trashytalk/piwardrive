import importlib
import subprocess
import sys
from pathlib import Path


def _setup_env() -> None:
    pass


def _build_c_plugin(plugin_dir: Path) -> None:
    src = plugin_dir / "cplugin.c"
    src.write_text(
        """
#define PY_SSIZE_T_CLEAN
#include <Python.h>

static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "cplugin",
    NULL,
    -1,
    NULL,
};

PyMODINIT_FUNC PyInit_cplugin(void) {
    PyObject *mod = PyModule_Create(&moduledef);
    if (!mod) return NULL;
    const char code[] =
        "from piwardrive.widgets.base import DashboardWidget\n"
        "class CWidget(DashboardWidget):\n"
        "    pass\n";
    PyObject *dict = PyModule_GetDict(mod);
    if (!dict) { Py_DECREF(mod); return NULL; }
    if (PyRun_String(code, Py_file_input, dict, dict) == NULL) {
        Py_DECREF(mod);
        return NULL;
    }
    return mod;
}
"""
    )
    suffix = subprocess.check_output(
        [
            sys.executable,
            "-c",
            "import sysconfig,sys;sys.stdout.write(sysconfig.get_config_var('EXT_SUFFIX'))",
        ],
        text=True,
    ).strip()
    includes = (
        subprocess.check_output(["python3-config", "--includes"], text=True)
        .strip()
        .split()
    )
    ldflags = (
        subprocess.check_output(["python3-config", "--ldflags"], text=True)
        .strip()
        .split()
    )
    subprocess.check_call(
        [
            "gcc",
            "-shared",
            "-fPIC",
            *includes,
            str(src),
            *ldflags,
            "-o",
            str(plugin_dir / f"cplugin{suffix}"),
        ]
    )


def test_plugin_discovery(tmp_path, monkeypatch):
    _setup_env()
    plugin_dir = tmp_path / ".config" / "piwardrive" / "plugins"
    plugin_dir.mkdir(parents=True)
    plugin_file = plugin_dir / "my_widget.py"
    plugin_file.write_text(
        "from piwardrive.widgets.base import DashboardWidget\n"
        "class ExtraWidget(DashboardWidget):\n"
        "    pass\n"
    )
    monkeypatch.setenv("HOME", str(tmp_path))
    sys.modules.pop("piwardrive.widgets", None)
    widgets = importlib.import_module("piwardrive.widgets")
    assert hasattr(widgets, "ExtraWidget")
    assert "ExtraWidget" in widgets.__all__


def test_cython_pyo3_plugin(tmp_path, monkeypatch):
    _setup_env()
    plugin_dir = tmp_path / ".config" / "piwardrive" / "plugins"
    plugin_dir.mkdir(parents=True)
    _build_c_plugin(plugin_dir)
    monkeypatch.setenv("HOME", str(tmp_path))
    sys.modules.pop("piwardrive.widgets", None)
    widgets = importlib.import_module("piwardrive.widgets")
    assert hasattr(widgets, "CWidget")
    assert "CWidget" in widgets.__all__


def test_load_error(tmp_path, monkeypatch):
    _setup_env()
    plugin_dir = tmp_path / ".config" / "piwardrive" / "plugins"
    plugin_dir.mkdir(parents=True)
    broken = plugin_dir / "broken.so"
    broken.write_bytes(b"\x00\x01\x02")
    messages: list[str] = []
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setattr("utils.report_error", lambda m: messages.append(m))
    sys.modules.pop("piwardrive.widgets", None)
    importlib.import_module("piwardrive.widgets")
    assert messages
