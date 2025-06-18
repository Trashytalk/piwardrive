import json
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import piwardrive.scripts.service_status as ss


def test_service_status_script_output(monkeypatch, capsys):
    monkeypatch.setattr(ss.diagnostics, "get_service_statuses", lambda svcs=None: {"kismet": True, "gpsd": False})
    ss.main(["kismet", "gpsd"])
    out = capsys.readouterr().out.strip()
    assert json.loads(out) == {"kismet": True, "gpsd": False}

