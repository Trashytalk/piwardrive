"""Entry point for the configuration helpers.

Similar to other stubs, this module ensures the ``src`` directory is available
on ``sys.path`` when running directly from the repository.  It then re-exports
all symbols from :mod:`piwardrive.config`."""

from __future__ import annotations

import os
import sys

SRC_PATH = os.path.join(os.path.dirname(__file__), "src")
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

from piwardrive.config import *  # noqa: F401,F403
