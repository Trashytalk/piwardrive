"""Print current orientation sensor values."""

from __future__ import annotations

import argparse
import json
import logging

from piwardrive import orientation_sensors as osens
from piwardrive.logconfig import setup_logging


def main(argv: list[str] | None = None) -> None:
    """Output orientation string, angle and raw sensor data."""
    parser = argparse.ArgumentParser(
        description="Show readings from orientation sensors"
    )
    parser.parse_args(argv)

    setup_logging(stdout=True)

    orient = osens.get_orientation_dbus()
    angle = None
    accel = gyro = None
    if orient:
        angle = osens.orientation_to_angle(orient)
    else:
        data = osens.read_mpu6050()
        if data:
            accel = data.get("accelerometer")
            gyro = data.get("gyroscope")

    logging.info(
        json.dumps(
            {
                "orientation": orient,
                "angle": angle,
                "accelerometer": accel,
                "gyroscope": gyro,
            }
        )
    )


if __name__ == "__main__":  # pragma: no cover - manual invocation
    main()
