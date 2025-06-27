import os
import sys
import types
from dataclasses import dataclass


@dataclass
class HealthRecord:
    timestamp: str
    cpu_temp: float | None
    cpu_percent: float
    memory_percent: float
    disk_percent: float

mod = types.ModuleType('piwardrive.persistence')
mod.HealthRecord = HealthRecord
sys.modules['piwardrive.persistence'] = mod
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

import uvicorn

import piwardrive.aggregation_service as m

uvicorn.run(m.app, host='127.0.0.1', port=int(os.environ['PORT']))
