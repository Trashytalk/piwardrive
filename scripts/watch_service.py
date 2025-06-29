"""Restart a systemd unit whenever watched files change."""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
from typing import Iterable

from watchgod import awatch

from piwardrive.logconfig import setup_logging
from piwardrive.utils import run_service_cmd


async def _restart(service: str) -> None:
    ok, _out, err = await asyncio.to_thread(run_service_cmd, service, "restart")
    if ok:
        logging.info("Restarted %s.service", service)
    else:
        logging.error("Failed to restart %s.service: %s", service, err.strip())


async def _watch(paths: Iterable[str], service: str) -> None:
    for p in paths:
        logging.info("Watching %s", os.path.abspath(p))
    async for _changes in awatch(*paths):
        await _restart(service)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Restart a systemd service whenever files change."
    )
    parser.add_argument(
        "paths",
        nargs="*",
        default=["src"],
        help="Directories to watch (default: src)",
    )
    parser.add_argument(
        "--service",
        default="piwardrive",
        help="Name of the systemd service to restart (default: piwardrive)",
    )
    args = parser.parse_args(argv)
    setup_logging(stdout=True)
    try:
        asyncio.run(_watch(args.paths, args.service))
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":  # pragma: no cover - manual invocation
    main()
