"""Public entry points for R integrations."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Optional

from .errors import PiWardriveError


def health_summary(path: str, plot_path: Optional[str] = None) -> Dict[str, float]:
    """Return averages using ``health_summary.R`` via rpy2."""
    try:
        from rpy2 import robjects
    except Exception as exc:  # pragma: no cover - rpy2 optional
        raise PiWardriveError("rpy2 is required for R integration") from exc

    r_script = Path(__file__).parent / "scripts" / "health_summary.R"
    robjects.r.source(str(r_script))
    r_func = robjects.globalenv["health_summary"]
    _result = r_func(path, plot_path if plot_path is not None else robjects.NULL)
    return dict(zip(_result.names, map(float, list(_result))))


__all__ = ["health_summary"]
