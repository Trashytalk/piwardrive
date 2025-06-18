import os
import sys
import types

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def test_obd_check_script(monkeypatch, capsys):
    class DummyResp:
        def __init__(self, value):
            self.value = value

    class DummyConn:
        def __init__(self):
            self.queries = []

        def is_connected(self):
            return True

        def port_name(self):
            return "/dev/mock"

        def query(self, cmd):
            self.queries.append(cmd)
            return DummyResp(cmd + "_val")

    dummy_conn = DummyConn()
    dummy_obd = types.SimpleNamespace(
        OBD=lambda port=None: dummy_conn,
        commands=types.SimpleNamespace(SPEED="SPEED", RPM="RPM", ENGINE_LOAD="LOAD"),
    )

    if "scripts.obd_check" in sys.modules:
        del sys.modules["scripts.obd_check"]
    import scripts.obd_check as oc

    monkeypatch.setattr(oc, "obd", dummy_obd)

    oc.main(["--port", "/dev/mock"])
    out_lines = capsys.readouterr().out.strip().splitlines()
    assert "connected" in out_lines[0]
    assert "SPEED_val" in out_lines[1]
    assert "RPM_val" in out_lines[2]
    assert "LOAD_val" in out_lines[3]
