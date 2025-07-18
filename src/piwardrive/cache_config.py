"""Lightweight loader for cache configuration."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

_CACHE_CONFIG_PATH = (
    Path(__file__).resolve().parents[2] / "config" / "cache_config.json"
)
_cache_data: Dict[str, Any] | None = None


def load_cache_config() -> Dict[str, Any]:
    """Return cache configuration dictionary if available."""
    global _cache_data
    if _cache_data is None:
        try:
            with open(_CACHE_CONFIG_PATH, "r", encoding="utf-8") as f:
                _cache_data = json.load(f)
        except FileNotFoundError:
            _cache_data = {}
    return _cache_data


__all__ = ["load_cache_config"]
