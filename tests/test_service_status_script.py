import json

import piwardrive.scripts.service_status as ss


def test_service_status_script_output(monkeypatch, capsys):
    monkeypatch.setattr(
        ss.diagnostics,
        "get_service_statuses",
        lambda svcs=None: {"kismet": True, "gpsd": False},
    )
    ss.main(["kismet", "gpsd"])
    out_lines = [
        json.loads(l) for l in capsys.readouterr().out.strip().splitlines() if l
    ]
    assert out_lines[-1]["message"] == json.dumps({"kismet": True, "gpsd": False})
