"""Verify that translation keys across locale files are synchronized."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def main(argv: list[str] | None = None) -> int:
    """Return ``0`` if all locale files contain the same keys."""
    locale_dir = Path(__file__).resolve().parents[1] / "locales"
    files = sorted(locale_dir.glob("*.json"))
    if not files:
        print("No locale files found", file=sys.stderr)
        return 1

    with open(files[0], "r", encoding="utf-8") as fh:
        try:
            baseline = set(json.load(fh))
        except Exception as exc:  # pragma: no cover - parse error
            print(f"{files[0].name} failed to parse: {exc}", file=sys.stderr)
            return 1

    failed = False
    for path in files[1:]:
        try:
            with open(path, "r", encoding="utf-8") as fh:
                keys = set(json.load(fh))
        except Exception as exc:  # pragma: no cover - parse error
            print(f"{path.name} failed to parse: {exc}", file=sys.stderr)
            failed = True
            continue

        missing = sorted(baseline - keys)
        extra = sorted(keys - baseline)
        if missing or extra:
            print(f"{path.name} is not synchronized", file=sys.stderr)
            if missing:
                print(f"  missing: {', '.join(missing)}", file=sys.stderr)
            if extra:
                print(f"  extra: {', '.join(extra)}", file=sys.stderr)
            failed = True

    if failed:
        return 1

    print("Locales are synchronized")
    return 0


if __name__ == "__main__":  # pragma: no cover - manual invocation
    raise SystemExit(main())
