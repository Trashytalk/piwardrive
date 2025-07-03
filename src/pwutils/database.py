"""Database export utilities."""

from __future__ import annotations

from typing import Sequence

from piwardrive import export, persistence


async def export_ap_cache(
    path: str,
    fmt: str,
    fields: Sequence[str] | None = None,
) -> None:
    """Export Wi-Fi observations to ``path`` using ``fmt``."""
    records = await persistence.load_ap_cache()
    export.export_records(records, path, fmt, fields)
