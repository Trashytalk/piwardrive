from importlib import import_module
import sys

_real = import_module("piwardrive.integrations.sigint_suite")
# Mirror the public attributes of the real package
globals().update(_real.__dict__)
sys.modules.setdefault(__name__, _real)
