"""Command line utility for viewing or updating PiWardrive configuration."""

from __future__ import annotations

import argparse
import asyncio
import json
from dataclasses import asdict
from typing import Any

import piwardrive.config as cfg
from piwardrive.core.config import _parse_env_value

try:
    import httpx
except Exception:  # pragma: no cover - optional dependency
    httpx = None


def _parse_value(raw: str, default: Any) -> Any:
    """Return ``raw`` converted to the type of ``default``."""
    try:
        return _parse_env_value(raw, default)
    except Exception:
        return raw


async def _api_get(base: str) -> dict:
    if httpx is None:
        raise RuntimeError("httpx required for API access")
    async with httpx.AsyncClient() as client:
        resp = await client.get(base.rstrip("/") + "/config")
        resp.raise_for_status()
        return resp.json()


async def _api_update(base: str, updates: dict) -> dict:
    if httpx is None:
        raise RuntimeError("httpx required for API access")
    async with httpx.AsyncClient() as client:
        resp = await client.post(base.rstrip("/") + "/config", json=updates)
        resp.raise_for_status()
        return resp.json()


def main(argv: list[str] | None = None) -> None:
    """Entry point for the ``config-cli`` command."""
    parser = argparse.ArgumentParser(description="Get or set configuration values")
    parser.add_argument("--url", help="Base URL of the running API")
    sub = parser.add_subparsers(dest="cmd")

    g = sub.add_parser("get", help="print the current value of KEY")
    g.add_argument("key")

    s = sub.add_parser("set", help="update KEY to VALUE")
    s.add_argument("key")
    s.add_argument("value")

    args = parser.parse_args(argv)

    if args.cmd == "get":
        if args.url:
            _data = asyncio.run(_api_get(args.url))
            if args.key not in _data:
                parser.error(f"Unknown key: {args.key}")
            print(json.dumps(_data[args.key]))
        else:
            _data = asdict(cfg.load_config())
            if args.key not in _data:
                parser.error(f"Unknown key: {args.key}")
            print(json.dumps(_data[args.key]))
    elif args.cmd == "set":
        if args.url:
            _data = asyncio.run(_api_get(args.url))
            if args.key not in _data:
                parser.error(f"Unknown key: {args.key}")
            value = _parse_value(args.value, _data[args.key])
            updated = asyncio.run(_api_update(args.url, {args.key: value}))
            print(json.dumps(updated[args.key]))
        else:
            cfg_data = asdict(cfg.load_config())
            if args.key not in cfg_data:
                parser.error(f"Unknown key: {args.key}")
            cfg_data[args.key] = _parse_value(args.value, cfg_data[args.key])
            cfg.save_config(cfg.Config(**cfg_data))
            print(json.dumps(cfg_data[args.key]))
    else:
        parser.print_help()


if __name__ == "__main__":  # pragma: no cover - manual invocation
    main()
