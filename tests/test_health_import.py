import os
import os
import sys
import json
import csv
import asyncio

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import scripts.health_import as hi
import persistence
import config


def setup_tmp(tmp_path):
    config.CONFIG_DIR = str(tmp_path)


def test_import_json(tmp_path):
    setup_tmp(tmp_path)
    data = [{
        "timestamp": "t",
        "cpu_temp": 1.0,
        "cpu_percent": 2.0,
        "memory_percent": 3.0,
        "disk_percent": 4.0,
    }]
    path = tmp_path / "data.json"
    path.write_text(json.dumps(data))
    hi.main([str(path), "--format", "json"])
    rows = asyncio.run(persistence.load_recent_health(1))
    assert rows and rows[0].cpu_percent == 2.0


def test_import_csv(tmp_path):
    setup_tmp(tmp_path)
    path = tmp_path / "data.csv"
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=[
            "timestamp",
            "cpu_temp",
            "cpu_percent",
            "memory_percent",
            "disk_percent",
        ])
        writer.writeheader()
        writer.writerow({
            "timestamp": "t",
            "cpu_temp": 1.0,
            "cpu_percent": 2.0,
            "memory_percent": 3.0,
            "disk_percent": 4.0,
        })
    hi.main([str(path), "--format", "csv"])
    rows = asyncio.run(persistence.load_recent_health(1))
    assert rows and rows[0].memory_percent == 3.0
