#!/usr/bin/env python3
"""Serve the local LexCode policy playground with only Python's standard library."""

from __future__ import annotations

import json
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from lexcode.policy import evaluate_policy  # noqa: E402


class PlaygroundHandler(BaseHTTPRequestHandler):
    server_version = "LexCodePlayground/1.0"

    def log_message(self, format_string: str, *args: object) -> None:
        return

    def _send(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self'")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, status: int, value: object) -> None:
        body = json.dumps(value, indent=2).encode("utf-8")
        self._send(status, body, "application/json; charset=utf-8")

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/api/data":
            self._json(
                200,
                {
                    "policy": self._read_json(ROOT / "lexcode/dsl/sample_internal_policy.json"),
                    "valid": self._read_json(ROOT / "tests/valid_arch.calm.json"),
                    "invalid": self._read_json(ROOT / "tests/invalid_arch.calm.json"),
                },
            )
            return
        static_files = {
            "/": (ROOT / "web/index.html", "text/html; charset=utf-8"),
            "/app.js": (ROOT / "web/app.js", "text/javascript; charset=utf-8"),
            "/style.css": (ROOT / "web/style.css", "text/css; charset=utf-8"),
        }
        item = static_files.get(path)
        if item is None:
            self._send(404, b"Not found", "text/plain; charset=utf-8")
            return
        file_path, content_type = item
        self._send(200, file_path.read_bytes(), content_type)

    @staticmethod
    def _read_json(path: Path) -> dict:
        with path.open(encoding="utf-8") as source:
            return json.load(source)

    def do_POST(self) -> None:
        if urlparse(self.path).path != "/api/evaluate":
            self._send(404, b"Not found", "text/plain; charset=utf-8")
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 1_000_000:
                self._json(413, {"error": "Request must contain at most one megabyte."})
                return
            request = json.loads(self.rfile.read(length))
            architecture = request.get("architecture")
            if not isinstance(architecture, dict):
                raise ValueError("architecture must be a JSON object")
            policy = self._read_json(ROOT / "lexcode/dsl/sample_internal_policy.json")
            self._json(200, evaluate_policy(policy, architecture))
        except (json.JSONDecodeError, UnicodeDecodeError, ValueError, TypeError) as error:
            self._json(400, {"error": str(error)})


def main() -> None:
    host = "127.0.0.1"
    port = int(os.environ.get("PORT", "8501"))
    server = ThreadingHTTPServer((host, port), PlaygroundHandler)
    print(f"LexCode playground running at http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
