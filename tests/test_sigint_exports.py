import csv
import json
import os
import sys

from piwardrive.sigint_suite.exports import export_csv, export_json, export_yaml


def test_export_csv(tmp_path):
    records = [{"a": "1", "b": "2"}]
    out = tmp_path / "data.csv"
    export_csv(records, str(out))
    rows = list(csv.DictReader(open(out)))
    assert rows == records


def test_export_yaml(tmp_path):
    records = [{"a": 1, "b": 2}]
    out = tmp_path / "data.yaml"
    export_yaml(records, str(out))
    import yaml

    loaded = yaml.safe_load(open(out))
    assert loaded == records


def test_all_contains_export_yaml():
    import piwardrive.sigint_suite.exports as ex

    assert "export_yaml" in ex.__all__


def test_export_json(tmp_path):
    records = [{"a": 1}, {"a": 2}]
    out = tmp_path / "data.json"
    export_json(records, str(out))
    data = json.load(open(out))
    assert data == records
