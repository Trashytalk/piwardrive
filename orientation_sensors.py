"""Entry point for orientation_sensors module."""
from importlib import import_module
import sys

module = import_module("piwardrive.orientation_sensors")
sys.modules[__name__] = module
