"""Entry point for persistence module."""
from piwardrive.persistence import *  # noqa: F401,F403
from piwardrive import persistence as _p

_get_conn = _p._get_conn  # type: ignore[attr-defined]
flush_health_records = _p.flush_health_records  # type: ignore[attr-defined]
