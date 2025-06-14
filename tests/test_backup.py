import os
import os
import sys
import tarfile
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import backup
import config


class DummyScheduler:
    def __init__(self) -> None:
        self.scheduled: list[tuple[str, float]] = []

    def schedule(self, name: str, cb, interval: float) -> None:
        self.scheduled.append((name, interval))
        cb(0)

    def cancel(self, name: str) -> None:
        pass


def setup_cfg(tmp_path: Path) -> config.AppConfig:
    config.CONFIG_DIR = str(tmp_path / 'cfg')
    config.CONFIG_PATH = str(Path(config.CONFIG_DIR) / 'config.json')
    cfg = config.AppConfig.load()
    cfg.kismet_logdir = str(tmp_path / 'logs')
    cfg.backup_dir = str(tmp_path / 'backups')
    cfg.backup_interval = 1
    os.makedirs(cfg.kismet_logdir, exist_ok=True)
    Path(cfg.kismet_logdir, 'dummy.txt').write_text('data')
    config.save_config(config.Config())
    return cfg


def test_create_and_restore_backup(tmp_path: Path) -> None:
    cfg = setup_cfg(tmp_path)
    archive = backup.create_backup(cfg.backup_dir, cfg)
    assert os.path.isfile(archive)
    # modify
    Path(config.CONFIG_PATH).write_text('changed')
    Path(cfg.kismet_logdir, 'dummy.txt').write_text('new')
    backup.restore_backup(archive, cfg)
    assert Path(config.CONFIG_PATH).read_text().startswith('{')
    assert Path(cfg.kismet_logdir, 'dummy.txt').read_text() == 'data'


def test_schedule_backups_calls_scheduler(tmp_path: Path) -> None:
    cfg = setup_cfg(tmp_path)
    sched = DummyScheduler()
    backup.schedule_backups(sched, cfg)
    assert sched.scheduled and sched.scheduled[0][0] == 'backup'
    assert sched.scheduled[0][1] == cfg.backup_interval

