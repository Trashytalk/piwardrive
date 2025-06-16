import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sigint_suite.exports import export_json


def test_export_json(tmp_path):
    records = [{"a": 1, "b": 2}]
    out = tmp_path / "data.json"
    export_json(records, str(out))
    assert json.load(open(out)) == records
