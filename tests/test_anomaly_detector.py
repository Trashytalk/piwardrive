import logging

from piwardrive.analytics.anomaly import HealthAnomalyDetector
from piwardrive.persistence import HealthRecord


def test_anomaly_warning_triggered(caplog):
    detector = HealthAnomalyDetector()
    records = [
        HealthRecord("t1", 40.0, 10.0, 20.0, 30.0),
        HealthRecord("t2", 41.0, 11.0, 21.0, 31.0),
        HealthRecord("t3", 39.5, 9.0, 19.0, 29.0),
    ]
    detector.fit(records)

    caplog.set_level(logging.WARNING)
    detector(HealthRecord("tx", 90.0, 50.0, 20.0, 30.0))
    assert any("anomaly" in rec.message.lower() for rec in caplog.records)
