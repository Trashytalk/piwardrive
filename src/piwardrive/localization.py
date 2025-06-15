"""Simple localization helper."""
import json
import os
from typing import Dict

_current = os.getenv("PW_LANG", "en")
_translations: Dict[str, Dict[str, str]] = {}


def set_locale(locale: str) -> None:
    """Load translations for ``locale`` and set as current."""
    global _current
    _current = locale
    if locale not in _translations:
        path = os.path.join(os.path.dirname(__file__), "locales", f"{locale}.json")
        try:
            with open(path, "r", encoding="utf-8") as f:
                _translations[locale] = json.load(f)
        except Exception:
            _translations[locale] = {}


def translate(key: str) -> str:
    """Return translated string for ``key`` or ``key`` if missing."""
    lang = _translations.get(_current)
    if lang is None:
        set_locale(_current)
        lang = _translations.get(_current, {})
    return lang.get(key, key)


# Convenience alias for use in code and KV files
_ = translate
