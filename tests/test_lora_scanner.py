import os
import sys
import asyncio
import json
from types import ModuleType
import pytest


from piwardrive import lora_scanner


def test_parse_packets():
    lines = [
        "time=2024-01-01T00:00:00Z freq=868.1 rssi=-120 snr=7.5 devaddr=ABC",
        "time=2024-01-01T00:00:01Z freq=868.1 rssi=-118 snr=6.8 devaddr=ABC",
    ]
    packets = lora_scanner.parse_packets(lines)
    assert len(packets) == 2
    assert packets[0].freq == 868.1
    assert packets[0].rssi == -120
    assert packets[0].devaddr == "ABC"


def test_plot_signal_trend(tmp_path, monkeypatch):
    path = tmp_path / "trend.png"
    packets = [
        lora_scanner.LoRaPacket("t1", 868.1, -120, 7.5, "A", ""),
        lora_scanner.LoRaPacket("t2", 868.1, -118, 6.8, "A", ""),
    ]

    mpl = ModuleType("matplotlib")
    mpl.use = lambda *a, **k: None
    pyplot = ModuleType("matplotlib.pyplot")
    pyplot.figure = lambda *a, **k: None
    pyplot.plot = lambda *a, **k: None
    pyplot.xlabel = lambda *a, **k: None
    pyplot.ylabel = lambda *a, **k: None
    pyplot.tight_layout = lambda *a, **k: None
    pyplot.savefig = lambda p, *a, **k: open(p, "wb").close()
    pyplot.close = lambda *a, **k: None
    mpl.pyplot = pyplot
    monkeypatch.setitem(sys.modules, "matplotlib", mpl)
    monkeypatch.setitem(sys.modules, "matplotlib.pyplot", pyplot)

    lora_scanner.plot_signal_trend(packets, str(path))
    assert path.is_file()


def test_async_scan_lora(monkeypatch):
    async def fake_exec(*_a, **_k):
        class P:
            async def communicate(self):
                return b"a\nb\n", b""

        return P()

    monkeypatch.setattr(asyncio, "create_subprocess_exec", fake_exec)
    lines = asyncio.run(lora_scanner.async_scan_lora("l0"))
    assert lines == ["a", "b"]


def test_async_parse_packets():
    lines = [
        "time=2024-01-01T00:00:00Z freq=868.1 rssi=-120 snr=7.5 devaddr=ABC",
        "time=2024-01-01T00:00:01Z freq=868.1 rssi=-118 snr=6.8 devaddr=ABC",
    ]
    packets = asyncio.run(lora_scanner.async_parse_packets(lines))
    assert len(packets) == 2


def test_main(capsys, monkeypatch):
    monkeypatch.setattr(lora_scanner, "scan_lora", lambda iface="l0": ["x"])
    argv = sys.argv
    sys.argv = ["prog"]
    try:
        lora_scanner.main()
    finally:
        sys.argv = argv
    out_lines = [
        json.loads(l) for l in capsys.readouterr().out.strip().splitlines() if l
    ]
    assert any(rec["message"] == "x" for rec in out_lines)

