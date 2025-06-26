"""Compatibility package for CLI scripts."""
import os
import sys
from pathlib import Path

# ``piwardrive.scripts`` acts as a thin wrapper around the top level ``scripts``
# directory that contains the actual CLI implementations.  Historically the
# project used a `src` layout which places the package under ``src/piwardrive``
# while CLI utilities live in ``scripts`` at the repository root.  The previous
# path calculation accidentally pointed to ``src/scripts`` which does not exist
# resulting in ``ModuleNotFoundError`` when importing submodules such as
# ``piwardrive.scripts.tile_maintenance_cli``.  Compute the correct path by
# navigating four directories upwards from this file to reach the repository
# root and then appending ``scripts``.
SCRIPTS_DIR = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "scripts")
)
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)
__path__ = [SCRIPTS_DIR]
