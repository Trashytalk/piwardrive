"""Export PiWardrive data to a MySQL/MariaDB database."""

import argparse
import asyncio
import os
from typing import Any

try:
    from persistence import load_ap_cache, load_recent_health  # type: ignore
except Exception:  # pragma: no cover - fallback
    from piwardrive.persistence import load_ap_cache, load_recent_health

from piwardrive.mysql_export import MySQLConfig, export_data


def _env_default(name: str, default: Any) -> Any:
    raw = os.getenv(name)
    if raw is None:
        return default
    if isinstance(default, int):
        try:
            return int(raw)
        except Exception:
            return default
    return raw


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Export data to MySQL/MariaDB")
    parser.add_argument("--host", default=_env_default("PW_MYSQL_HOST", "localhost"))
    parser.add_argument("--port", type=int, default=_env_default("PW_MYSQL_PORT", 3306))
    parser.add_argument("--user", default=_env_default("PW_MYSQL_USER", "piwardrive"))
    parser.add_argument("--password", default=_env_default("PW_MYSQL_PASSWORD", ""))
    parser.add_argument("--database", default=_env_default("PW_MYSQL_DB", "piwardrive"))
    parser.add_argument(
        "--limit", "-n", type=int, default=1000, help="Health record limit"
    )
    args = parser.parse_args(argv)

    cfg = MySQLConfig(
        host=args.host,
        port=args.port,
        user=args.user,
        password=args.password,
        database=args.database,
    )

    health, wifi = asyncio.run(
        asyncio.gather(load_recent_health(args.limit), load_ap_cache())
    )
    asyncio.run(export_data(cfg, health, wifi))


if __name__ == "__main__":  # pragma: no cover - manual invocation
    main()
