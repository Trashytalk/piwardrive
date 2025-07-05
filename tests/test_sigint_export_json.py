import json

from piwardrive.sigint_suite.exports import export_json


def test_export_json(tmp_path):
    records = [{"a": 1, "b": 2}]
    out = tmp_path / "data.json"
    export_json(records, str(out))
    assert json.load(open(out)) == records
