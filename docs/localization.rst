:orphan:

Localization
============
.. note::
   Please read the legal notice in the project `README.md` before using PiWardrive.

PiWardrive translates interface labels using JSON files under ``locales/``.
Each file is named after a two-letter ISO 639-1 code such as ``en.json`` or
``es.json``.  ``PW_LANG`` selects the desired language at runtime and defaults
to ``en``.

Adding a Language
-----------------

1. Copy ``locales/en.json`` to ``<code>.json`` where ``<code>`` is the new
   language code. Translate the values while keeping all keys intact.
2. Update existing locale files whenever new strings are added. ``en.json``
   should always contain the complete set of keys.
3. Run ``scripts/update_translations.sh`` to generate
   ``locales/piwardrive.pot`` using gettext.
4. Run ``python scripts/check_locales_sync.py`` to verify that all locale
   files share the same keys. The script exits with a non-zero status if any
   differences are found.
5. Set ``PW_LANG`` or call ``localization.set_locale()`` to switch languages.

These steps keep the translations synchronized and avoid missing strings in the
UI.
