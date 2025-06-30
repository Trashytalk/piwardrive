import json
import sqlite3
import sys


def test_db_summary_script(tmp_path, capsys):
    db_path = tmp_path / "health.db"
    with sqlite3.connect(db_path) as db:
        db.execute("CREATE TABLE health_records (timestamp TEXT)")
        db.execute("CREATE TABLE ap_cache (bssid TEXT)")
        db.execute("INSERT INTO health_records VALUES ('t1')")
        db.execute("INSERT INTO ap_cache VALUES ('b1')")
        db.commit()

    if "piwardrive.scripts.db_summary" in sys.modules:
        del sys.modules["piwardrive.scripts.db_summary"]
    import piwardrive.scripts.db_summary as ds

    ds.main([str(db_path), "--json"])
    out = json.loads(capsys.readouterr().out)
    assert out["health_records"] == 1
    assert out["ap_cache"] == 1
