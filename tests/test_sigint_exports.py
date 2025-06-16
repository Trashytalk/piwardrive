import os
import sys
import csv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sigint_suite.exports import export_csv


def test_export_csv(tmp_path):
    records = [{"a": "1", "b": "2"}]
    out = tmp_path / "data.csv"
    export_csv(records, str(out))
    rows = list(csv.DictReader(open(out)))
    assert rows == records
