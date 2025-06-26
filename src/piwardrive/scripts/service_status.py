"""Command line helper for checking systemd service status."""
import argparse
import json
from types import SimpleNamespace


def _get_service_statuses(services=None):
    """Import :mod:`piwardrive.diagnostics` lazily and get statuses."""
    from piwardrive import diagnostics as _diag
    return _diag.get_service_statuses(services)


diagnostics = SimpleNamespace(get_service_statuses=_get_service_statuses)


def main(argv: list[str] | None = None) -> None:
    """Print active states for the given systemd services."""
    parser = argparse.ArgumentParser(description="Show systemd service status")
    parser.add_argument(
        "services",
        nargs="*",
        help="Services to check (defaults to kismet, bettercap, gpsd)",
    )
    args = parser.parse_args(argv)
    statuses = diagnostics.get_service_statuses(args.services or None)
    print(json.dumps(statuses))


if __name__ == "__main__":  # pragma: no cover - manual invocation
    main()
