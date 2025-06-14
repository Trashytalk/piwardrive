import os
import tarfile
from datetime import datetime

import config
from config import AppConfig
from scheduler import PollScheduler

DEFAULT_BACKUP_DIR = os.path.join(os.path.expanduser("~"), ".config", "piwardrive", "backups")


def _backup_items(cfg: AppConfig) -> list[tuple[str, str]]:
    """Return (path, arcname) pairs for files/dirs to backup."""
    items = []
    if os.path.exists(config.CONFIG_PATH):
        items.append((config.CONFIG_PATH, 'config.json'))
    if os.path.isdir(cfg.kismet_logdir):
        items.append((cfg.kismet_logdir, 'kismet_logs'))
    return items


def create_backup(backup_dir: str | None = None, cfg: AppConfig | None = None) -> str:
    """Create a ``.tar.gz`` archive of configuration and logs."""
    cfg = cfg or AppConfig.load()
    backup_dir = backup_dir or cfg.backup_dir
    os.makedirs(backup_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    archive = os.path.join(backup_dir, f'backup-{timestamp}.tar.gz')
    with tarfile.open(archive, 'w:gz') as tar:
        for path, name in _backup_items(cfg):
            tar.add(path, arcname=name)
    return archive


def restore_backup(archive_path: str, cfg: AppConfig | None = None) -> None:
    """Restore configuration and logs from ``archive_path``."""
    cfg = cfg or AppConfig.load()
    with tarfile.open(archive_path, 'r:gz') as tar:
        for member in tar.getmembers():
            if member.name == 'config.json':
                os.makedirs(os.path.dirname(config.CONFIG_PATH), exist_ok=True)
                tar.extract(member, os.path.dirname(config.CONFIG_PATH))
                os.replace(
                    os.path.join(os.path.dirname(config.CONFIG_PATH), 'config.json'),
                    config.CONFIG_PATH,
                )
            elif member.name.startswith('kismet_logs'):
                if os.path.exists(cfg.kismet_logdir):
                    import shutil
                    shutil.rmtree(cfg.kismet_logdir, ignore_errors=True)
                base = os.path.dirname(cfg.kismet_logdir)
                os.makedirs(base, exist_ok=True)
                tar.extract(member, base)
                extracted = os.path.join(base, 'kismet_logs')
                if os.path.exists(extracted) and extracted != cfg.kismet_logdir:
                    os.replace(extracted, cfg.kismet_logdir)


def schedule_backups(sched: PollScheduler, cfg: AppConfig | None = None) -> None:
    """Schedule periodic backups using ``sched``."""
    cfg = cfg or AppConfig.load()
    sched.schedule('backup', lambda _dt: create_backup(cfg.backup_dir, cfg), cfg.backup_interval)
