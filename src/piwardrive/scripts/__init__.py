"""Compatibility package for CLI scripts."""
import os
import sys
from pathlib import Path

# Add the top level ``scripts`` directory to ``sys.path`` so that test modules
# can import ``piwardrive.scripts.*``.  ``__file__`` is
# ``src/piwardrive/scripts/__init__.py`` so ``parents[3]`` resolves to the
# repository root.
SCRIPTS_DIR = str(Path(__file__).resolve().parents[3] / "scripts")
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)
__path__ = [SCRIPTS_DIR]
