"""Entry point for gpsd_client module."""
from importlib import import_module
import sys

module = import_module("piwardrive.gpsd_client")
sys.modules[__name__] = module
