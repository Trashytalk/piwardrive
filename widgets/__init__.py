from importlib import import_module, sys

module = import_module("piwardrive.widgets")
sys.modules[__name__] = module
