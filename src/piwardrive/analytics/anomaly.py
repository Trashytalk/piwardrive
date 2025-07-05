from __future__ import annotations

"""Anomaly detection for health records."""

import logging
from typing import Iterable

from sklearn.ensemble import IsolationForest

from ..persistence import HealthRecord


class HealthAnomalyDetector:
    """Detect anomalies in CPU temperature and usage."""

    def __init__(self, contamination: float = 0.05) -> None:
        self._model = IsolationForest(contamination=contamination, random_state=0)
        self._fitted = False

    def fit(self, records: Iterable[HealthRecord]) -> None:
        """Train the detector on historical ``records``."""
        data = [[r.cpu_temp, r.cpu_percent] for r in records if r.cpu_temp is not None]
        if not data:
            self._fitted = False
            return
        self._model.fit(data)
        self._fitted = True

    def __call__(self, record: HealthRecord) -> None:
        """Invoke the detector with ``record`` and log warnings for anomalies."""
        if not self._fitted or record.cpu_temp is None:
            return
        pred = self._model.predict([[record.cpu_temp, record.cpu_percent]])
        if pred[0] == -1:
            logging.warning(
                "Health anomaly detected: temp=%s cpu=%s",
                record.cpu_temp,
                record.cpu_percent,
            )


__all__ = ["HealthAnomalyDetector"]
