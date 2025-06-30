"""Simple SQLite database browser."""

from __future__ import annotations

import http.server
import json
import logging
import sqlite3
from pathlib import Path


class _DBHandler(http.server.BaseHTTPRequestHandler):
    db_path: Path

    def do_GET(self):  # pragma: no cover - simple HTTP handler
        try:
            with sqlite3.connect(self.db_path) as conn:
                cur = conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                )
                tables = [r[0] for r in cur.fetchall()]
                data = {
                    # The table names come from sqlite_master and are not user supplied
                    t: conn.execute(f"SELECT * FROM {t} LIMIT 100").fetchall()  # nosec B608
                    for t in tables
                }
        except sqlite3.Error as exc:
            logging.error("Database access failed: %s", exc)
            self.send_error(500, f"Database error: {exc}")
            return

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data, default=str).encode())


def launch_browser(db_path: str, port: int = 8080, host: str = "127.0.0.1") -> None:
    """Start a simple HTTP server exposing the contents of ``db_path``."""
    handler = type("Handler", (_DBHandler,), {"db_path": Path(db_path)})
    try:
        server = http.server.HTTPServer((host, port), handler)
    except OSError as exc:
        logging.error("Failed to start HTTP server: %s", exc)
        return
    server.serve_forever()
