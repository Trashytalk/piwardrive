import argparse
import asyncio
import sqlite3
from typing import Any


def _create_tables(conn: sqlite3.Connection) -> None:
    conn.execute(
        """CREATE TABLE IF NOT EXISTS health_metrics (
            timestamp TEXT,
            cpu_temp REAL,
            cpu_percent REAL,
            memory_percent REAL,
            disk_percent REAL
        )"""
    )
    conn.execute(
        """CREATE TABLE IF NOT EXISTS wifi_observations (
            bssid TEXT,
            ssid TEXT,
            encryption TEXT,
            lat REAL,
            lon REAL,
            last_time INTEGER
        )"""
    )


def _insert_health(conn: sqlite3.Connection, records: list[Any]) -> None:
    conn.executemany(
        (
            "INSERT INTO health_metrics VALUES "
            "(:timestamp, :cpu_temp, :cpu_percent, :memory_percent, :disk_percent)"
        ),
        [r.__dict__ for r in records],
    )


def _insert_wifi(conn: sqlite3.Connection, records: list[dict[str, Any]]) -> None:
    conn.executemany(
        (
            "INSERT INTO wifi_observations VALUES "
            "(:bssid, :ssid, :encryption, :lat, :lon, :last_time)"
        ),
        records,
    )


async def _load_data(limit: int) -> tuple[list[Any], list[dict[str, Any]]]:
    try:
        from persistence import load_ap_cache, load_recent_health  # type: ignore
    except Exception:  # pragma: no cover - fallback
        from piwardrive.persistence import load_ap_cache, load_recent_health

    health = await load_recent_health(limit)
    wifi = await load_ap_cache()
    return health, wifi


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Export PiWardrive data for Grafana")
    parser.add_argument("output", help="destination SQLite file")
    parser.add_argument(
        "--limit", "-n", type=int, default=1000, help="health record limit"
    )
    args = parser.parse_args(argv)

    health, wifi = asyncio.run(_load_data(args.limit))
    conn = sqlite3.connect(args.output)
    _create_tables(conn)
    _insert_health(conn, health)
    _insert_wifi(conn, wifi)
    conn.commit()
    conn.close()


if __name__ == "__main__":  # pragma: no cover - manual invocation
    main()
