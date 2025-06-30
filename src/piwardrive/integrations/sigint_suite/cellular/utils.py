from __future__ import annotations

import os
import shlex
from typing import List, Optional, Tuple


def build_cmd_args(
    cmd: Optional[str],
    env_cmd: str,
    default_cmd: str,
    timeout: Optional[int],
    env_timeout: str,
) -> tuple[list[str], int]:
    """Return command args list and timeout for scanner helpers."""
    cmd_str = str(cmd or os.getenv(env_cmd, default_cmd))
    args = shlex.split(cmd_str)
    timeout_val = timeout if timeout is not None else int(os.getenv(env_timeout, "10"))
    return args, timeout_val
