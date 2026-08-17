"""Unauthenticated, attachment-only file sharing for the H4G site."""

from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
import threading
import time
import uuid
from collections import defaultdict, deque
from datetime import datetime, timezone
from email.utils import formatdate
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, quote, unquote, urlparse


HOST = os.getenv("FILESHARE_HOST", "127.0.0.1")
PORT = int(os.getenv("FILESHARE_PORT", "8789"))
MAX_FILE_BYTES = int(os.getenv("FILESHARE_MAX_FILE_BYTES", str(100 * 1024 * 1024)))
MAX_TOTAL_BYTES = int(os.getenv("FILESHARE_MAX_TOTAL_BYTES", str(10 * 1024 * 1024 * 1024)))
RATE_LIMIT = int(os.getenv("FILESHARE_RATE_LIMIT", "30"))
RATE_WINDOW = int(os.getenv("FILESHARE_RATE_WINDOW", "3600"))
DATA_DIR = Path(os.getenv("FILESHARE_DATA_DIR", "/var/lib/h4g-fileshare"))
FILES_DIR = DATA_DIR / "files"
INDEX_FILE = DATA_DIR / "index.json"
VAULT_ROOT = Path(__file__).resolve().parents[2]
ID_PATTERN = re.compile(r"^[0-9a-f]{32}$")
LOCK = threading.RLock()
REQUESTS: dict[str, deque[float]] = defaultdict(deque)


def clean_filename(value: str) -> str:
    """Keep a display/download name, never a filesystem path."""
    value = unquote(value).replace("\\", "/").split("/")[-1]
    value = "".join(char for char in value if char >= " " and char not in '\x7f\r\n"')
    value = re.sub(r"\s+", " ", value).strip(" .")
    if not value:
        value = "upload.bin"
    stem, suffix = os.path.splitext(value)
    if len(value.encode("utf-8")) > 240:
        suffix = suffix[:32]
        budget = max(1, 220 - len(suffix.encode("utf-8")))
        stem = stem.encode("utf-8")[:budget].decode("utf-8", "ignore")
        value = stem + suffix
    return value


def load_index() -> dict:
    if not INDEX_FILE.exists():
        return {"files": []}
    try:
        value = json.loads(INDEX_FILE.read_text(encoding="utf-8"))
        return value if isinstance(value.get("files"), list) else {"files": []}
    except (OSError, json.JSONDecodeError):
        return {"files": []}


def save_index(value: dict) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix="index-", suffix=".json", dir=DATA_DIR)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(value, stream, ensure_ascii=False, separators=(",", ":"))
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, INDEX_FILE)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def current_usage(index: dict) -> int:
    return sum(int(item.get("size", 0)) for item in index["files"])


class Handler(BaseHTTPRequestHandler):
    server_version = "H4GFileShare/1.0"

    def security_headers(self) -> None:
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Content-Security-Policy", "default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self'; base-uri 'none'; frame-ancestors 'none'")

    def send_json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.security_headers()
        self.end_headers()
        self.wfile.write(body)

    def send_static(self, path: Path, content_type: str) -> None:
        body = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-cache")
        self.security_headers()
        self.end_headers()
        self.wfile.write(body)

    def client_key(self) -> str:
        return self.headers.get("X-Forwarded-For", self.client_address[0]).split(",")[0].strip()

    def rate_limited(self) -> bool:
        now, bucket = time.monotonic(), REQUESTS[self.client_key()]
        while bucket and now - bucket[0] > RATE_WINDOW:
            bucket.popleft()
        if len(bucket) >= RATE_LIMIT:
            return True
        bucket.append(now)
        return False

    def listing(self) -> dict:
        with LOCK:
            index = load_index()
            files = [item for item in index["files"] if ID_PATTERN.fullmatch(str(item.get("id", ""))) and (FILES_DIR / item["id"]).is_file()]
            files.sort(key=lambda item: item.get("uploaded_at", ""), reverse=True)
            usage = sum(int(item.get("size", 0)) for item in files)
        return {"files": files, "usage_bytes": usage, "max_file_bytes": MAX_FILE_BYTES, "max_total_bytes": MAX_TOTAL_BYTES}

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/health":
            self.send_json(200, {"status": "ok", "storage": str(DATA_DIR)})
        elif path in {"/fileshare", "/fileshare/"}:
            self.send_static(VAULT_ROOT / "fileshare" / "index.html", "text/html; charset=utf-8")
        elif path == "/fileshare/app.js":
            self.send_static(VAULT_ROOT / "fileshare" / "app.js", "text/javascript; charset=utf-8")
        elif path == "/api/fileshare":
            self.send_json(200, self.listing())
        elif path.startswith("/api/fileshare/download/"):
            self.download(path.rsplit("/", 1)[-1])
        else:
            self.send_json(404, {"error": "Not found"})

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path != "/api/fileshare":
            self.send_json(404, {"error": "Not found"}); return
        if self.rate_limited():
            self.send_json(429, {"error": "Upload rate limit exceeded. Try again later."}); return
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            length = 0
        if length <= 0:
            self.send_json(411, {"error": "A non-empty Content-Length is required."}); return
        if length > MAX_FILE_BYTES:
            self.send_json(413, {"error": f"File exceeds the {MAX_FILE_BYTES} byte upload limit."}); return
        filename = clean_filename(parse_qs(parsed.query).get("filename", [""])[0])
        file_id = uuid.uuid4().hex
        FILES_DIR.mkdir(parents=True, exist_ok=True)
        temporary = FILES_DIR / f".{file_id}.upload"
        digest = hashlib.sha256()
        try:
            with LOCK:
                index = load_index()
                if current_usage(index) + length > MAX_TOTAL_BYTES:
                    self.send_json(507, {"error": "The shared storage quota is full."}); return
                remaining = length
                with temporary.open("xb") as stream:
                    while remaining:
                        chunk = self.rfile.read(min(1024 * 1024, remaining))
                        if not chunk:
                            raise ValueError("Upload ended before Content-Length bytes were received.")
                        stream.write(chunk)
                        digest.update(chunk)
                        remaining -= len(chunk)
                    stream.flush()
                    os.fsync(stream.fileno())
                os.replace(temporary, FILES_DIR / file_id)
                item = {"id": file_id, "name": filename, "size": length, "sha256": digest.hexdigest(), "uploaded_at": datetime.now(timezone.utc).isoformat()}
                index["files"].append(item)
                try:
                    save_index(index)
                except Exception:
                    (FILES_DIR / file_id).unlink(missing_ok=True)
                    raise
            self.send_json(201, {"file": item})
        except ValueError as error:
            temporary.unlink(missing_ok=True)
            self.send_json(400, {"error": str(error)})
        except Exception:
            temporary.unlink(missing_ok=True)
            self.send_json(500, {"error": "Unable to store the file."})

    def download(self, file_id: str) -> None:
        if not ID_PATTERN.fullmatch(file_id):
            self.send_json(404, {"error": "File not found"}); return
        with LOCK:
            item = next((entry for entry in load_index()["files"] if entry.get("id") == file_id), None)
        path = FILES_DIR / file_id
        if not item or not path.is_file():
            self.send_json(404, {"error": "File not found"}); return
        size = path.stat().st_size
        safe_ascii = re.sub(r"[^A-Za-z0-9._ -]", "_", item["name"]) or "download.bin"
        self.send_response(200)
        self.send_header("Content-Type", "application/octet-stream")
        self.send_header("Content-Length", str(size))
        self.send_header("Content-Disposition", f"attachment; filename=\"{safe_ascii}\"; filename*=UTF-8''{quote(item['name'])}")
        self.send_header("Last-Modified", formatdate(path.stat().st_mtime, usegmt=True))
        self.send_header("Cache-Control", "private, no-store")
        self.security_headers()
        self.end_headers()
        with path.open("rb") as stream:
            while chunk := stream.read(1024 * 1024):
                self.wfile.write(chunk)

    def log_message(self, fmt: str, *args) -> None:
        print(f"{self.address_string()} - {fmt % args}")


def main() -> None:
    print(f"File share listening on http://{HOST}:{PORT}; max file {MAX_FILE_BYTES:,} bytes; quota {MAX_TOTAL_BYTES:,} bytes")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()


if __name__ == "__main__":
    main()
