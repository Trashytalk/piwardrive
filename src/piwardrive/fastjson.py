"""Fast JSON helpers with optional accelerators.

This module exposes :func:`loads` and :func:`dumps` backed by the fastest
available library. The import order is:

1. ``orjson`` – preferred if installed.
2. ``ujson`` – used when ``orjson`` is unavailable.
3. builtin ``json`` – final fallback.
"""

from __future__ import annotations

import json
from typing import Any

try:  # pragma: no cover - optional dependency
    import orjson as _json
except Exception:  # pragma: no cover - orjson missing
    try:
        import ujson as _json
    except Exception:  # pragma: no cover - fallback
        _json = json


def loads(data: bytes | str) -> Any:
    """Deserialize JSON ``data`` using the chosen backend."""
    return _json.loads(data)


def dumps(obj: Any, **kwargs: Any) -> str:
    """Serialize ``obj`` to JSON using the chosen backend."""
    result = _json.dumps(obj, **kwargs)
    if isinstance(result, bytes):
        return result.decode()
    return result


__all__ = ["loads", "dumps"]
