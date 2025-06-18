import os
import sys
import importlib
import subprocess
from pathlib import Path



def _setup_kivy(add_dummy_module):
    add_dummy_module(
        "kivy.uix.behaviors", DragBehavior=type("DragBehavior", (), {})
    )
    add_dummy_module(
        "kivymd.uix.boxlayout", MDBoxLayout=type("MDBoxLayout", (), {})
    )


def _build_c_plugin(plugin_dir: Path) -> None:
    src = plugin_dir / "cplugin.c"
    src.write_text(
        "#define PY_SSIZE_T_CLEAN\n"
        "#include <Python.h>\n\n"
        "static struct PyModuleDef moduledef = {\n"
        "    PyModuleDef_HEAD_INIT,\n"
        "    \"cplugin\",\n"
        "    NULL,\n"
        "    -1,\n"
        "    NULL,\n"
        "};\n\n"
        "PyMODINIT_FUNC PyInit_cplugin(void) {\n"
        "    PyObject *mod = PyModule_Create(&moduledef);\n"
        "    if (!mod) return NULL;\n"
        "    const char code[] =\n"
        "        \"from piwardrive.widgets.base import DashboardWidget\\n\"\n"
        "        \"class CWidget(DashboardWidget):\\n\"\n"
        "        \"    pass\\n\";\n"
        "    PyObject *dict = PyModule_GetDict(mod);\n"
        "    if (!dict) { Py_DECREF(mod); return NULL; }\n"
        "    if (PyRun_String(code, Py_file_input, dict, dict) == NULL) {\n"
        "        Py_DECREF(mod);\n"
        "        return NULL;\n"
        "    }\n"
        "    return mod;\n"
        "}\n"
    )
    suffix = subprocess.check_output(
        [sys.executable, "-c", "import sysconfig,sys;sys.stdout.write(sysconfig.get_config_var('EXT_SUFFIX'))"],
        text=True,
    ).strip()
    includes = subprocess.check_output(
        ["python3-config", "--includes"], text=True
    ).strip().split()
    ldflags = subprocess.check_output(
        ["python3-config", "--ldflags"], text=True
    ).strip().split()
    subprocess.check_call([
        "gcc",
        "-shared",
        "-fPIC",
        *includes,
        str(src),
        *ldflags,
        "-o",
        str(plugin_dir / f"cplugin{suffix}"),
    ])


def test_plugin_discovery(tmp_path, monkeypatch, add_dummy_module):
    _setup_kivy(add_dummy_module)
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


def test_cython_pyo3_plugin(tmp_path, monkeypatch, add_dummy_module):
    _setup_kivy(add_dummy_module)
    plugin_dir = tmp_path / ".config" / "piwardrive" / "plugins"
    plugin_dir.mkdir(parents=True)
    _build_c_plugin(plugin_dir)

    monkeypatch.setenv("HOME", str(tmp_path))
    sys.modules.pop("piwardrive.widgets", None)
    widgets = importlib.import_module("piwardrive.widgets")
    assert hasattr(widgets, "CWidget")
    assert "CWidget" in widgets.__all__


def test_load_error(tmp_path, monkeypatch, add_dummy_module):
    _setup_kivy(add_dummy_module)
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

