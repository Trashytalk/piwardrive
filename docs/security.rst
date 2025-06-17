Security Guidance
-----------------
.. note::
   Please read the legal notice in the project `README.md` before using PiWardrive.

The :mod:`security` module exposes helpers for sanitising paths, validating service names and hashing passwords. ``hash_password`` derives a PBKDF2‑HMAC‑SHA256 digest with a random salt while ``verify_password`` recomputes the hash and compares it in constant time. Store only the hashed value in ``config.json`` or the ``PW_ADMIN_PASSWORD_HASH`` environment variable. Never commit plain text passwords to version control.

To generate a hash run::

    python -c "import security,sys; print(security.hash_password(sys.argv[1]))" mypass

Keep the resulting string in a protected location such as ``~/.config/piwardrive/config.json`` or a secrets manager. The verification helper is tolerant of bad input and simply returns ``False`` on failure.
