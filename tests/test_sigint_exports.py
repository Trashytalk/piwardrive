import os
import sys
import csv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sigint_suite.exports import export_csv, export_yaml


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
    import sigint_suite.exports as ex

    assert "export_yaml" in ex.__all__
