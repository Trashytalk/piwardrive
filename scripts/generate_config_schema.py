#!/usr/bin/env python3
"""Generate JSON schema for :class:`piwardrive.core.config.ConfigModel`."""
from __future__ import annotations

import json
from pathlib import Path

from piwardrive.core.config import ConfigModel


def main(dest: str = "docs/config_schema.json") -> None:
    """Write ConfigModel schema to ``dest``."""
    schema = ConfigModel.model_json_schema()
    Path(dest).write_text(json.dumps(schema, indent=2))


if __name__ == "__main__":  # pragma: no cover - manual use
    main()
