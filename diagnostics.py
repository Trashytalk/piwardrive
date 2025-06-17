"""Entry point for diagnostics module."""
from importlib import import_module
import sys

module = import_module("piwardrive.diagnostics")
sys.modules[__name__] = module
