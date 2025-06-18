from importlib import import_module
import sys
module = import_module("piwardrive.scripts")
sys.modules[__name__] = module
