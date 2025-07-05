import gc

from piwardrive.memory_monitor import MemoryMonitor


def test_memory_monitor_detects_growth():
    mon = MemoryMonitor(history=2, threshold_mb=0.0)
    first = mon.sample()
    _data = [bytearray(1024 * 1024)]  # allocate ~1MB
    gc.collect()
    second = mon.sample()
    assert second >= first
    mon.stop()
