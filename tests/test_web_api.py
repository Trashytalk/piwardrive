import sys
from types import ModuleType
from fastapi.testclient import TestClient

# Provide dummy modules for widgets
mods = {
    "kivy.uix.behaviors": ModuleType("behaviors"),
    "kivymd.uix.boxlayout": ModuleType("boxlayout"),
}
mods["kivy.uix.behaviors"].DragBehavior = type("DragBehavior", (), {})
mods["kivymd.uix.boxlayout"].MDBoxLayout = type("MDBoxLayout", (), {})
for name, mod in mods.items():
    sys.modules[name] = mod

from piwardrive import widgets
from piwardrive.web_api import app


def test_widget_endpoint_lists_classes():
    client = TestClient(app)
    resp = client.get("/api/widgets")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    # Should include at least one known widget
    assert "BatteryStatusWidget" in data

