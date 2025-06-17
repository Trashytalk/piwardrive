from importlib import import_module, sys
module = import_module("piwardrive.sigint_suite")
sys.modules[__name__] = module
