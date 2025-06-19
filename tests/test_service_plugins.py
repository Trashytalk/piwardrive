import importlib
from fastapi.testclient import TestClient

from piwardrive import service


def test_plugins_endpoint(tmp_path, monkeypatch, add_dummy_module):
    # Setup dummy Kivy modules so plugin import works
    add_dummy_module("kivy.uix.behaviors", DragBehavior=type("DragBehavior", (), {}))
    add_dummy_module("kivymd.uix.boxlayout", MDBoxLayout=type("MDBoxLayout", (), {}))

    plugin_dir = tmp_path / ".config" / "piwardrive" / "plugins"
    plugin_dir.mkdir(parents=True)
    plugin_file = plugin_dir / "plug.py"
    plugin_file.write_text(
        "from piwardrive.widgets.base import DashboardWidget\n"
        "class TestPlugin(DashboardWidget):\n"
        "    pass\n"
    )

    monkeypatch.setenv("HOME", str(tmp_path))

    import piwardrive.widgets as widgets
    importlib.reload(widgets)
    importlib.reload(service)

    client = TestClient(service.app)
    resp = client.get("/plugins")
    assert resp.status_code == 200
    assert "TestPlugin" in resp.json()
