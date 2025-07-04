#!/usr/bin/env python
"""Generate OpenAPI schema for the PiWardrive API."""

from __future__ import annotations

import argparse
import json

import os
import sys

SRC_PATH = os.path.join(os.path.dirname(__file__), os.pardir, "src")
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

from piwardrive import service


def main() -> None:
    parser = argparse.ArgumentParser(description="Write OpenAPI schema to file")
    parser.add_argument(
        "-o", "--output", default="openapi.json", help="Output file path"
    )
    args = parser.parse_args()
    schema = service.app.openapi()
    with open(args.output, "w", encoding="utf-8") as fh:
        json.dump(schema, fh, indent=2)


if __name__ == "__main__":  # pragma: no cover - manual usage
    main()
