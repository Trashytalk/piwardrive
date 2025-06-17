"""Entry point for utils module."""
from importlib import import_module
import sys

module = import_module("piwardrive.utils")
sys.modules[__name__] = module
