"""Entry point for :mod:`piwardrive.main` when running from the repo."""
from __future__ import annotations
import os
import sys

SRC_PATH = os.path.join(os.path.dirname(__file__), "src")
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

from piwardrive.main import PiWardriveApp as _BaseApp


class PiWardriveApp(_BaseApp):
    """Thin wrapper that exposes :class:`~piwardrive.main.PiWardriveApp`."""

    def control_service(self, svc: str, action: str) -> None:  # pragma: no cover - logic tested via wrapper
        """Run a systemctl command for a given service with retries."""
        import os
        import getpass as _getpass
        from piwardrive.security import (
            verify_password as _verify,
            validate_service_name as _validate,
        )

        cfg = getattr(self, "config_data", None)
        cfg_hash = getattr(cfg, "admin_password_hash", "")
        pw = os.getenv("PW_ADMIN_PASSWORD")
        if not pw:
            try:
                pw = _getpass.getpass("Password: ")
            except Exception:
                pw = ""
        if cfg_hash and not _verify(pw or "", cfg_hash):
            utils.report_error("Unauthorized")
            return
        try:
            _validate(svc)
        except ValueError as exc:
            utils.report_error(str(exc))
            return
        try:
            success, _out, err = self._run_service_cmd(svc, action, attempts=3, delay=1)
        except Exception as exc:  # pragma: no cover - subprocess failures
            utils.report_error(f"Failed to {action} {svc}: {exc}")
            return
        if not success:
            msg = err.strip() if isinstance(err, str) else err
            utils.report_error(f"Failed to {action} {svc}: {msg or 'Unknown error'}")
            return
        if action in {"start", "restart"} and not utils.ensure_service_running(svc):
            utils.report_error(f"{svc} failed to stay running after {action}")
