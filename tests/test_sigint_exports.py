import os
import sys
import csv
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sigint_suite.exports import export_csv, export_json


def test_export_csv(tmp_path):
    records = [{"a": "1", "b": "2"}]
    out = tmp_path / "data.csv"
    export_csv(records, str(out))
    rows = list(csv.DictReader(open(out)))
    assert rows == records


def test_export_json(tmp_path):
    records = [{"a": 1}, {"a": 2}]
    out = tmp_path / "data.json"
    export_json(records, str(out))
    data = json.load(open(out))
    assert data == records
