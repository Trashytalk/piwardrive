"""Module service_status."""
import argparse
import json

from piwardrive import diagnostics


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
