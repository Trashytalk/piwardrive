"""Compatibility package for CLI scripts."""
import os
import sys

SCRIPTS_DIR = os.path.normpath(
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "scripts")
)
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)
__path__ = [SCRIPTS_DIR]
