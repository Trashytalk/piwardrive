"""Simple SQLite database browser."""

from __future__ import annotations

import http.server
import json
import sqlite3
from pathlib import Path


class _DBHandler(http.server.BaseHTTPRequestHandler):
    db_path: Path

    def do_GET(self):  # pragma: no cover - simple HTTP handler
        conn = sqlite3.connect(self.db_path)
        cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [r[0] for r in cur.fetchall()]
        data = {
            # The table names come from sqlite_master and are not user supplied
            t: conn.execute(f"SELECT * FROM {t} LIMIT 100").fetchall()  # nosec B608
            for t in tables
        }

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data, default=str).encode())
        conn.close()


def launch_browser(db_path: str, port: int = 8080, host: str = "127.0.0.1") -> None:
    """Start a simple HTTP server exposing the contents of ``db_path``."""
    handler = type("Handler", (_DBHandler,), {"db_path": Path(db_path)})
    server = http.server.HTTPServer((host, port), handler)
    server.serve_forever()
