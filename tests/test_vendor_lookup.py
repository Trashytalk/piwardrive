import os
import sys
import types
import importlib

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sigint_suite import paths


def _reload_module(monkeypatch, tmp_path):
    monkeypatch.setenv("SIGINT_CONFIG_DIR", str(tmp_path))
    if "sigint_suite.enrichment.oui" in sys.modules:
        monkeypatch.delitem(sys.modules, "sigint_suite.enrichment.oui", raising=False)
    return importlib.import_module("sigint_suite.enrichment.oui")


def test_update_oui_file_downloads(monkeypatch, tmp_path):
    oui = _reload_module(monkeypatch, tmp_path)
    csv_data = "Assignment,Organization Name\nAA-BB-CC,VendorX\n"

    class Resp:
        content = csv_data.encode()

        def raise_for_status(self):
            pass

    monkeypatch.setattr(oui.requests, "get", lambda url, timeout=15: Resp())
    oui.update_oui_file(max_age=0, path=oui.OUI_PATH)
    assert os.path.isfile(oui.OUI_PATH)
    vendor = oui.lookup_vendor("AA:BB:CC:00:11:22")
    assert vendor == "VendorX"

    called = False

    def fail(*a, **k):
        nonlocal called
        called = True
        raise AssertionError

    monkeypatch.setattr(oui.requests, "get", fail)
    vendor2 = oui.lookup_vendor("AA:BB:CC:33:44:55")
    assert vendor2 == "VendorX" and not called

