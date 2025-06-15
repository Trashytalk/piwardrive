"""Simple localization helper."""
import json
import os
from functools import lru_cache
from typing import Dict

_current = os.getenv("PW_LANG", "en")


@lru_cache(maxsize=None)
def _load_locale(locale: str) -> Dict[str, str]:
    """Read the JSON file for ``locale`` and cache the parsed result."""
    path = os.path.join(os.path.dirname(__file__), "locales", f"{locale}.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def set_locale(locale: str) -> None:
    """Set ``locale`` as current and cache its translations."""
    global _current
    _current = locale
    _load_locale(locale)


def translate(key: str) -> str:
    """Return translated string for ``key`` or ``key`` if missing."""
    lang = _load_locale(_current)
    return lang.get(key, key)


# Convenience alias for use in code and KV files
_ = translate
