import asyncio
from datetime import datetime
from pathlib import Path

from piwardrive import persistence


def setup_tmp(tmp_path: Path) -> None:
    persistence.config.CONFIG_DIR = str(tmp_path)


def test_save_and_load_fingerprint_info(tmp_path: Path) -> None:
    setup_tmp(tmp_path)
    info = persistence.FingerprintInfo(
        environment="test",
        source="file",
        record_count=5,
        created_at=datetime.now().isoformat(),
    )
    asyncio.run(persistence.save_fingerprint_info(info))
    rows = asyncio.run(persistence.load_fingerprint_info())
    assert rows and rows[0].environment == "test"
