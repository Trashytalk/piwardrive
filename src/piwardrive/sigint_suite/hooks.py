"""Module hooks."""
from collections import defaultdict
from typing import Any, Callable, Dict, List

# registry mapping data types to list of processors
_POST_PROCESSORS: Dict[
    str, List[Callable[[List[Dict[str, Any]]], List[Dict[str, Any]]]]
] = defaultdict(list)


def register_post_processor(
    data_type: str,
    func: Callable[[List[Dict[str, Any]]], List[Dict[str, Any]]],
) -> None:
    """Register ``func`` to post-process ``data_type`` records."""
    _POST_PROCESSORS[data_type].append(func)


def apply_post_processors(
    data_type: str, records: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """Apply registered processors for ``data_type`` to ``records``."""
    for func in _POST_PROCESSORS.get(data_type, []):
        try:
            records = list(func(records))
        except Exception:
            continue
    return records


__all__ = ["register_post_processor", "apply_post_processors"]
