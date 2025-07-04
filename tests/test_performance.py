from piwardrive import performance


def test_record_metrics() -> None:
    performance.clear()
    with performance.record("a"):
        pass
    metrics = performance.get_metrics()
    assert metrics["a"]["count"] == 1
