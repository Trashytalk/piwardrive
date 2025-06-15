import os
import sys
import time
from types import ModuleType, SimpleNamespace


class DummySession:
    def __init__(self, *a, **k) -> None:
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass

os.environ.setdefault("KIVY_NO_ARGS", "1")
os.environ.setdefault("KIVY_WINDOW", "mock")

modules = {
    "kivy.app": ModuleType("kivy.app"),
    "kivy.clock": ModuleType("kivy.clock"),
    "kivy.metrics": ModuleType("kivy.metrics"),
    "kivy.uix.label": ModuleType("kivy.uix.label"),
    "kivy.uix.screenmanager": ModuleType("kivy.uix.screenmanager"),
    "kivymd.uix.dialog": ModuleType("kivymd.uix.dialog"),
    "kivymd.uix.menu": ModuleType("kivymd.uix.menu"),
    "kivymd.uix.snackbar": ModuleType("kivymd.uix.snackbar"),
    "kivymd.uix.textfield": ModuleType("kivymd.uix.textfield"),
    "kivymd.uix.progressbar": ModuleType("kivymd.uix.progressbar"),
    "kivymd.uix.boxlayout": ModuleType("kivymd.uix.boxlayout"),
    "kivymd.uix.label": ModuleType("kivymd.uix.label"),
    "aiohttp": ModuleType("aiohttp"),
    "gps": ModuleType("gps"),
}
modules["aiohttp"].ClientSession = DummySession
modules["aiohttp"].ClientTimeout = lambda *a, **k: None
modules["aiohttp"].ClientError = Exception
modules["kivy.app"].App = type("App", (), {"get_running_app": staticmethod(lambda: None)})
modules["kivy.clock"].Clock = SimpleNamespace(create_trigger=lambda *a, **k: lambda *a2, **k2: None)
modules["kivy.clock"].mainthread = lambda f: f
modules["kivy.metrics"].dp = lambda x: x
modules["kivy.uix.label"].Label = object
modules["kivy.uix.screenmanager"].Screen = object
modules["kivymd.uix.dialog"].MDDialog = object
modules["kivymd.uix.menu"].MDDropdownMenu = object
modules["kivymd.uix.snackbar"].Snackbar = type("Snackbar", (), {"__init__": lambda self, *a, **k: None, "open": lambda self: None})
modules["kivymd.uix.textfield"].MDTextField = object
modules["kivymd.uix.progressbar"].MDProgressBar = object
modules["kivymd.uix.boxlayout"].MDBoxLayout = type("MDBoxLayout", (), {"__init__": lambda self, *a, **k: None, "add_widget": lambda self, *a, **k: None})
modules["kivymd.uix.label"].MDLabel = type("MDLabel", (), {"__init__": lambda self, *a, **k: None})

modules["kivy_garden.mapview"] = SimpleNamespace(
    MapMarker=object,
    MapMarkerPopup=object,
    MBTilesMapSource=object,
    LineMapLayer=object,
)

for name, mod in modules.items():
    sys.modules[name] = mod

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
if "screens.map_screen" in sys.modules:
    del sys.modules["screens.map_screen"]
from screens.map_screen import MapScreen  # noqa: E402


def test_prefetch_tiles_downloads(monkeypatch, tmp_path):
    screen = MapScreen()
    called = []

    async def fake_dl(_session, url, local):
        called.append(url)
        os.makedirs(os.path.dirname(local), exist_ok=True)
        with open(local, "wb") as fh:
            fh.write(b"data")

    monkeypatch.setattr(screen, "_download_tile_async", fake_dl)
    bounds = (0.0, 0.0, 1.0, 1.0)
    screen.prefetch_tiles(bounds, zoom=1, folder=str(tmp_path))
    assert len(called) == 2
    assert (tmp_path / "1" / "1" / "0.png").is_file()
    assert (tmp_path / "1" / "1" / "1.png").is_file()


def test_purge_old_tiles(tmp_path):
    screen = MapScreen()
    old = tmp_path / "old.txt"
    recent = tmp_path / "new.txt"
    old.write_text("x")
    recent.write_text("y")
    now = time.time()
    os.utime(old, (now - 90000, now - 90000))
    os.utime(recent, (now, now))
    screen.purge_old_tiles(max_age_days=1, folder=str(tmp_path))
    assert not old.exists()
    assert recent.exists()


def test_enforce_cache_limit(tmp_path):
    screen = MapScreen()
    files = []
    for i in range(3):
        p = tmp_path / f"f{i}.bin"
        with open(p, "wb") as fh:
            fh.write(b"x" * 1024)
        os.utime(p, (i, i))
        files.append(p)
    screen.enforce_cache_limit(folder=str(tmp_path), limit_mb=0.002)
    remaining = list(tmp_path.iterdir())
    assert len(remaining) == 2
    assert files[0] not in remaining
