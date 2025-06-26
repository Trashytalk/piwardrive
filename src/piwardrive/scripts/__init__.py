"""Compatibility package for CLI scripts."""
import os
import sys

# ``piwardrive.scripts`` acts as a thin wrapper around the top level ``scripts``
# directory that contains the actual CLI implementations.  Historically the
# project used a `src` layout which places the package under ``src/piwardrive``
# while CLI utilities live in ``scripts`` at the repository root.  The previous
# path calculation accidentally pointed to ``src/scripts`` which does not exist
# resulting in ``ModuleNotFoundError`` when importing submodules such as
# ``piwardrive.scripts.tile_maintenance_cli``.  Compute the correct path by
# navigating four directories upwards from this file to reach the repository
# root and then appending ``scripts``.
PACKAGE_DIR = os.path.dirname(__file__)
SCRIPTS_DIR = os.path.normpath(
    os.path.join(PACKAGE_DIR, "..", "..", "..", "scripts")
)
for _p in (PACKAGE_DIR, SCRIPTS_DIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)
__path__ = [PACKAGE_DIR, SCRIPTS_DIR]
