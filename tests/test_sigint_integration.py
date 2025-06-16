import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sigint_integration import load_sigint_data


def test_load_sigint_data(tmp_path):
    path = tmp_path / "exports"
    path.mkdir()
    data = [{"a": 1}, {"b": 2}]
    (path / "wifi.json").write_text(json.dumps(data))
    os.environ["SIGINT_EXPORT_DIR"] = str(path)
    try:
        recs = load_sigint_data("wifi")
        assert recs == data
    finally:
        os.environ.pop("SIGINT_EXPORT_DIR")


def test_load_sigint_data_missing(tmp_path):
    os.environ["SIGINT_EXPORT_DIR"] = str(tmp_path)
    try:
        assert load_sigint_data("wifi") == []
    finally:
        os.environ.pop("SIGINT_EXPORT_DIR")
