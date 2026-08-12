"""Dependency-free localhost HTTP API for the H4G Cipher Identifier."""

from __future__ import annotations

import json
import os
import time
from collections import defaultdict, deque
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from services.cipher_identifier.classifier import identify
from services.cipher_identifier.opencode_advisor import safe_advise


HOST = os.getenv("CIPHER_API_HOST", "127.0.0.1")
PORT = int(os.getenv("CIPHER_API_PORT", "8787"))
MAX_BODY = 24_000
RATE = int(os.getenv("CIPHER_RATE_LIMIT", "30"))
WINDOW = 60
REQUESTS: dict[str, deque] = defaultdict(deque)
VAULT_ROOT = Path(__file__).resolve().parents[2]


class Handler(BaseHTTPRequestHandler):
    server_version = "H4GCipherIdentifier/1.0"

    def send_json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode()
        self.send_response(status); self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body))); self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff"); self.end_headers(); self.wfile.write(body)

    def do_GET(self) -> None:
        if self.path == "/health":
            self.send_json(200, {"status": "ok", "ai_enabled": os.getenv("CIPHER_AI_ENABLED", "0").lower() in {"1", "true", "yes"}})
        elif self.path == "/cipher-identifier":
            self.send_response(301); self.send_header("Location", "/cipher-identifier/"); self.end_headers()
        elif self.path == "/cipher-identifier/":
            body = (VAULT_ROOT / "cipher-identifier" / "index.html").read_bytes()
            self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body))); self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers(); self.wfile.write(body)
        else:
            self.send_json(404, {"error": "Not found"})

    def do_POST(self) -> None:
        if self.path != "/api/cipher-identify": self.send_json(404, {"error": "Not found"}); return
        forwarded = self.headers.get("X-Forwarded-For", self.client_address[0]).split(",")[0].strip()
        now, bucket = time.monotonic(), REQUESTS[forwarded]
        while bucket and now - bucket[0] > WINDOW: bucket.popleft()
        if len(bucket) >= RATE: self.send_json(429, {"error": "Rate limit exceeded. Try again shortly."}); return
        bucket.append(now)
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > MAX_BODY: raise ValueError("Request body must be between 1 and 24,000 bytes.")
            payload = json.loads(self.rfile.read(length))
            ciphertext = payload.get("text", "")
            use_ai = bool(payload.get("use_ai", True))
            result = identify(ciphertext)
            result["ai"] = safe_advise(ciphertext, result) if use_ai else {"status": "skipped", "reason": "AI review not requested."}
            self.send_json(200, result)
        except (ValueError, TypeError, json.JSONDecodeError) as error: self.send_json(400, {"error": str(error)})
        except Exception: self.send_json(500, {"error": "Identification service error."})

    def log_message(self, fmt: str, *args) -> None:
        print(f"{self.address_string()} - {fmt % args}")


def main() -> None:
    print(f"Cipher identifier API listening on http://{HOST}:{PORT}")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()


if __name__ == "__main__": main()
