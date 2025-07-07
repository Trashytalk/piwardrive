"""Test module for running aggregation server with mock HealthRecord.

This module provides a mock HealthRecord class and runs the aggregation service
for testing purposes.
"""
import os
import sys
import types
from dataclasses import dataclass


@dataclass
class HealthRecord:
    """Mock HealthRecord class for testing aggregation service.
    
    Attributes:
        timestamp: Timestamp of the health record.
        cpu_temp: CPU temperature measurement, may be None.
        cpu_percent: CPU usage percentage.
        memory_percent: Memory usage percentage.
        disk_percent: Disk usage percentage.
    """

    timestamp: str
    cpu_temp: float | None
    cpu_percent: float
    memory_percent: float
    disk_percent: float


mod = types.ModuleType("piwardrive.persistence")
mod.HealthRecord = HealthRecord
sys.modules["piwardrive.persistence"] = mod
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

import uvicorn

import piwardrive.aggregation_service as m

uvicorn.run(m.app, host="127.0.0.1", port=int(os.environ["PORT"]))
