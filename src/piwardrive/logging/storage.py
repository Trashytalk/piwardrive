import asyncio
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict

import boto3


class StorageBackend:
    """Base class for storage backends."""

    async def upload(self, file_path: str, file_hash: str) -> bool:
        raise NotImplementedError


class LocalStorageBackend(StorageBackend):
    """Simple local filesystem archival."""

    def __init__(self, config: Dict[str, any]):
        self.path = config.get("path", "/tmp")
        os.makedirs(self.path, exist_ok=True)

    async def upload(self, file_path: str, file_hash: str) -> bool:
        dest = Path(self.path) / Path(file_path).name
        try:
            dest.write_bytes(Path(file_path).read_bytes())
            return True
        except Exception as exc:
            logging.error("Local archival failed for %s: %s", file_path, exc)
            return False


class SyslogStorageBackend(StorageBackend):
    """Placeholder backend that would forward logs to syslog."""

    def __init__(self, config: Dict[str, any]):
        self.address = config.get("address", "/dev/log")

    async def upload(self, file_path: str, file_hash: str) -> bool:
        logging.info("Syslog backend upload not implemented: %s", file_path)
        return False


class S3StorageBackend(StorageBackend):
    """AWS S3 storage backend for log archival."""

    def __init__(self, config: Dict[str, any]):
        self.config = config
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=config.get("access_key"),
            aws_secret_access_key=config.get("secret_key"),
            region_name=config.get("region", "us-east-1"),
        )
        self.bucket = config["bucket"]
        self.prefix = config.get("prefix", "")

    async def upload(self, file_path: str, file_hash: str) -> bool:
        try:
            timestamp = datetime.utcnow().strftime("%Y/%m/%d")
            filename = Path(file_path).name
            key = f"{self.prefix}{timestamp}/{filename}"
            self.s3_client.upload_file(
                file_path,
                self.bucket,
                key,
                ExtraArgs={
                    "Metadata": {
                        "file_hash": file_hash,
                        "upload_timestamp": datetime.utcnow().isoformat(),
                        "source_instance": os.uname().nodename,
                    },
                    "StorageClass": "STANDARD_IA",
                },
            )
            return True
        except Exception as exc:
            logging.error("Failed to upload %s to S3: %s", file_path, exc)
            return False


class LogArchiveManager:
    """Manages log archival to various storage backends."""

    def __init__(self, config: Dict[str, any]):
        self.config = config
        self.storage_backends = self._initialize_backends()
        self.executor = ThreadPoolExecutor(max_workers=4)

    def _initialize_backends(self) -> Dict[str, StorageBackend]:
        backends: Dict[str, StorageBackend] = {}
        for name, cfg in self.config.get("storage_backends", {}).items():
            if cfg.get("type") == "s3":
                backends[name] = S3StorageBackend(cfg)
            elif cfg.get("type") == "local":
                backends[name] = LocalStorageBackend(cfg)
            elif cfg.get("type") == "syslog":
                backends[name] = SyslogStorageBackend(cfg)
        return backends

    async def archive_log(self, log_file: str, backend_name: str) -> bool:
        if backend_name not in self.storage_backends:
            raise ValueError(f"Unknown storage backend: {backend_name}")
        backend = self.storage_backends[backend_name]
        file_hash = await self._calculate_file_hash(log_file)
        success = await backend.upload(log_file, file_hash)
        if success:
            await self._record_archival(log_file, backend_name, file_hash)
        return success

    async def _calculate_file_hash(self, file_path: str) -> str:
        import hashlib

        def _hash_file() -> str:
            h = hashlib.sha256()
            try:
                with open(file_path, "rb") as f:
                    for chunk in iter(lambda: f.read(4096), b""):
                        h.update(chunk)
            except OSError as exc:
                logging.exception("Failed to read %s for hashing: %s", file_path, exc)
                return ""
            return h.hexdigest()

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, _hash_file)

    async def _record_archival(
        self, log_file: str, backend_name: str, file_hash: str
    ) -> None:
        record_dir = Path(self.config.get("archive_metadata", "/tmp"))
        record_dir.mkdir(parents=True, exist_ok=True)
        meta = {
            "file": log_file,
            "backend": backend_name,
            "hash": file_hash,
            "timestamp": datetime.utcnow().isoformat(),
        }
        path = record_dir / f"{Path(log_file).name}.json"
        await asyncio.get_event_loop().run_in_executor(
            self.executor, path.write_text, str(meta)
        )


class LogRetentionManager:
    """Manages log retention policies and cleanup."""

    def __init__(self, config: Dict[str, any]):
        self.config = config
        self.retention_policies = self._load_retention_policies()

    def _load_retention_policies(self) -> Dict[str, Dict]:
        return {
            "application": {
                "local_retention_days": 7,
                "archive_retention_days": 90,
                "compliance_retention_days": 2555,
            },
            "security": {
                "local_retention_days": 30,
                "archive_retention_days": 365,
                "compliance_retention_days": 2555,
            },
            "performance": {
                "local_retention_days": 3,
                "archive_retention_days": 30,
                "compliance_retention_days": 365,
            },
        }

    async def cleanup_expired_logs(self, log_type: str) -> None:
        if log_type not in self.retention_policies:
            return
        policy = self.retention_policies[log_type]
        now = datetime.utcnow()
        local_cutoff = now - timedelta(days=policy["local_retention_days"])
        await self._cleanup_local_logs(log_type, local_cutoff)
        archive_cutoff = now - timedelta(days=policy["archive_retention_days"])
        await self._cleanup_archived_logs(log_type, archive_cutoff)

    async def _cleanup_local_logs(self, log_type: str, cutoff: datetime) -> None:
        directory = Path(self.config["log_directories"][log_type])
        for log_file in directory.glob("*.log*"):
            if log_file.stat().st_mtime < cutoff.timestamp():
                try:
                    log_file.unlink()
                    logging.info("Removed expired log file: %s", log_file)
                except Exception as exc:
                    logging.error("Failed to remove %s: %s", log_file, exc)

    async def _cleanup_archived_logs(self, log_type: str, cutoff: datetime) -> None:
        archive_dir = Path(self.config.get("archive_metadata", "/tmp"))
        for meta_file in archive_dir.glob("*.json"):
            try:
                _data = meta_file.read_text()
            except Exception:
                continue
            try:
                import json

                meta = json.loads(data)
            except Exception:
                continue
            ts = datetime.fromisoformat(meta.get("timestamp", "1970-01-01T00:00:00"))
            if ts < cutoff:
                try:
                    meta_file.unlink()
                except Exception:
                    pass
