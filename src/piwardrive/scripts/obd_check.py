"""Attempt basic OBD-II queries and print the results."""

from __future__ import annotations

import argparse

try:
    import obd  # type: ignore  # pragma: no cover - optional dependency
except Exception:  # pragma: no cover - library not available
    obd = None  # type: ignore


def main(argv: list[str] | None = None) -> None:
    """Connect to an OBD-II adapter and print sample readings."""
    parser = argparse.ArgumentParser(description="Check OBD-II connectivity")
    parser.add_argument("--port", help="serial port for the adapter", default=None)
    args = parser.parse_args(argv)

    if obd is None:
        print("python-OBD library not installed")
        return

    try:
        conn = obd.OBD(args.port)  # pragma: no cover - runtime
    except Exception as exc:  # pragma: no cover - runtime
        print(f"Connection failed: {exc}")
        return

    status = "connected" if conn.is_connected() else "disconnected"
    port_name = getattr(conn, "port_name", lambda: args.port)
    print(f"{status} on {port_name()}")

    if not conn.is_connected():
        return

    try:
        speed = conn.query(obd.commands.SPEED)
        rpm = conn.query(obd.commands.RPM)
        load = conn.query(obd.commands.ENGINE_LOAD)
        print(f"Speed: {speed.value}")
        print(f"RPM: {rpm.value}")
        print(f"Engine load: {load.value}")
    except Exception as exc:  # pragma: no cover - runtime
        print(f"Query failed: {exc}")


if __name__ == "__main__":  # pragma: no cover - manual invocation
    main()
