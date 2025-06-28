import time

from piwardrive.config_watcher import watch_config


def test_watch_config_triggers(tmp_path):
    path = tmp_path / "config.json"
    path.write_text("{}")
    triggered = []
    observer = watch_config(str(path), lambda: triggered.append("x"))
    try:
        time.sleep(0.1)
        path.write_text('{"a": 1}')
        for _ in range(20):
            if triggered:
                break
            time.sleep(0.1)
    finally:
        observer.stop()
        observer.join()
    assert triggered
