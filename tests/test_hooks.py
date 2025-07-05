from piwardrive.sigint_suite.hooks import register_post_processor  # noqa: E402
from piwardrive.sigint_suite.wifi.scanner import scan_wifi  # noqa: E402


def test_custom_post_processor(monkeypatch):
    output = """
Cell 01 - Address: AA:BB:CC:DD:EE:FF
          ESSID:"TestNet"
          Frequency:2.437 GHz (Channel 6)
          Quality=70/70  Signal level=-40 dBm
"""
    monkeypatch.setattr("subprocess.check_output", lambda *a, **k: output)

    # isolate hooks for this test
    import piwardrive.sigint_suite.hooks as hooks

    hooks._POST_PROCESSORS["wifi"] = []

    def add_custom(records):
        for r in records:
            r["added"] = "yes"
        return records

    register_post_processor("wifi", add_custom)

    nets = scan_wifi("wlan0")
    assert nets[0]["added"] == "yes"

    # restore default hooks
    hooks._POST_PROCESSORS["wifi"] = []
    from piwardrive.sigint_suite.wifi.scanner import _vendor_hook

    register_post_processor("wifi", _vendor_hook)
