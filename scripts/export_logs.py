"""Module export_logs."""
import argparse
import asyncio
from piwardrive.main import PiWardriveApp


def main(argv: list[str] | None = None) -> None:
    """Export recent application logs to a file."""
    parser = argparse.ArgumentParser(description="Export application logs")
    parser.add_argument("output", nargs="?", help="Output file path")
    parser.add_argument(
        "--lines",
        "-n",
        type=int,
        default=200,
        help="Number of log lines to export",
    )
    args = parser.parse_args(argv)

    app = PiWardriveApp()
    path = asyncio.run(app.export_logs(args.output, args.lines))
    if path:
        print(path)


if __name__ == "__main__":  # pragma: no cover - manual invocation
    main()
