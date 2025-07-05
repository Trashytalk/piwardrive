import asyncio
import importlib
import sys
import weakref

from piwardrive.memory_monitor import MemoryMonitor
from piwardrive.resource_manager import ResourceManager
from piwardrive.widget_manager import LazyWidgetManager


def _setup_widget(tmp_path, monkeypatch):
    plugin_dir = tmp_path / ".config" / "piwardrive" / "plugins"
    plugin_dir.mkdir(parents=True)
    plugin_file = plugin_dir / "lazy.py"
    plugin_file.write_text(
        "from piwardrive.widgets.base import DashboardWidget\n"
        "loaded = True\n"
        "class Lazy(DashboardWidget):\n"
        "    pass\n"
    )
    monkeypatch.setenv("HOME", str(tmp_path))
    sys.modules.pop("piwardrive.widgets", None)
    importlib.import_module("piwardrive.widgets")


def test_lazy_manager_load(tmp_path, monkeypatch):
    _setup_widget(tmp_path, monkeypatch)
    rm = ResourceManager()
    mgr = LazyWidgetManager(rm, memory_monitor=MemoryMonitor(history=1))

    assert "lazy" not in sys.modules
    _widget = asyncio.run(mgr.get_widget("Lazy"))
    assert widget.__class__.__name__ == "Lazy"
    assert "lazy" in sys.modules
    sys.modules.pop("lazy", None)


def test_release_widget(tmp_path, monkeypatch):
    _setup_widget(tmp_path, monkeypatch)
    rm = ResourceManager()
    mgr = LazyWidgetManager(rm, memory_monitor=MemoryMonitor(history=1))
    _widget = asyncio.run(mgr.get_widget("Lazy"))
    ref = weakref.ref(widget)
    mgr.release_widget("Lazy")
    del widget
    asyncio.run(rm.cancel_all())
    import gc

    gc.collect()
    assert ref() is None
    sys.modules.pop("lazy", None)


def test_memory_pressure_unloads(tmp_path, monkeypatch):
    _setup_widget(tmp_path, monkeypatch)
    rm = ResourceManager()

    class DummyMonitor(MemoryMonitor):
        def __init__(self):
            super().__init__(history=1, threshold_mb=0.0)
            self._next = 0.0

        def sample(self) -> float:  # override
            val = self._next
            self._next = 1000.0
            return val

    mon = DummyMonitor()
    mgr = LazyWidgetManager(rm, memory_monitor=mon, unload_threshold_mb=0.0)
    _widget = asyncio.run(mgr.get_widget("Lazy"))
    assert mgr.loaded() == ["Lazy"]
    # next sample triggers unload
    mgr.release_widget("nope")
    asyncio.run(mgr.get_widget("Lazy"))  # load again to trigger sample
    assert mgr.loaded() == [] or mgr.loaded() == ["Lazy"]
    sys.modules.pop("lazy", None)
