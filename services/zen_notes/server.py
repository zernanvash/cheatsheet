"""Unauthenticated, file-backed editing API for Zen CTF Notes."""

from __future__ import annotations

import html
import json
import os
import re
import tempfile
import threading
import time
from collections import defaultdict, deque
from datetime import datetime, timezone
from html.parser import HTMLParser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse


HOST = os.getenv("ZEN_NOTES_HOST", "127.0.0.1")
PORT = int(os.getenv("ZEN_NOTES_PORT", "8788"))
MAX_BODY = int(os.getenv("ZEN_NOTES_MAX_BODY", "262144"))
RATE = int(os.getenv("ZEN_NOTES_RATE_LIMIT", "30"))
WINDOW = 60
VAULT_ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = Path(os.getenv("ZEN_NOTES_DATA", "/var/lib/h4g-zen-notes/notes.json"))
REQUESTS: dict[str, deque] = defaultdict(deque)
LOCK = threading.Lock()
ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]{0,159}$")
ALLOWED_TAGS = {"a", "blockquote", "br", "code", "div", "em", "h1", "h2", "h3", "h4", "li", "ol", "p", "pre", "span", "strong", "table", "tbody", "td", "th", "thead", "tr", "ul"}
VOID_TAGS = {"br"}
ALLOWED_CLASSES = {"code", "code-head", "source", "table-wrap"}


def known_ids() -> set[str]:
    source = (VAULT_ROOT / "zen-ctf-notes" / "notes-data.js").read_text(encoding="utf-8")
    prefix = "window.ZEN_NOTES="
    if not source.startswith(prefix):
        raise RuntimeError("Invalid Zen notes data")
    return {item["id"] for item in json.loads(source[len(prefix):].rstrip(";"))}


class Sanitizer(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.stack: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag not in ALLOWED_TAGS:
            self.stack.append("")
            return
        clean: list[str] = []
        for name, value in attrs:
            if tag == "a" and name == "href" and value and (value.startswith("#") or value.startswith("https://") or value.startswith("http://")):
                clean.append(f'href="{html.escape(value, quote=True)}"')
            elif name == "class" and value:
                classes = " ".join(item for item in value.split() if item in ALLOWED_CLASSES)
                if classes:
                    clean.append(f'class="{classes}"')
        suffix = (" " + " ".join(clean)) if clean else ""
        self.parts.append(f"<{tag}{suffix}>")
        self.stack.append(tag)

    def handle_endtag(self, tag: str) -> None:
        if not self.stack:
            return
        opened = self.stack.pop()
        if opened and opened not in VOID_TAGS:
            self.parts.append(f"</{opened}>")

    def handle_data(self, data: str) -> None:
        self.parts.append(html.escape(data))

    def handle_entityref(self, name: str) -> None:
        self.parts.append(f"&{name};")

    def handle_charref(self, name: str) -> None:
        self.parts.append(f"&#{name};")


def sanitize_html(value: str) -> str:
    parser = Sanitizer()
    parser.feed(value)
    parser.close()
    while parser.stack:
        tag = parser.stack.pop()
        if tag and tag not in VOID_TAGS:
            parser.parts.append(f"</{tag}>")
    return "".join(parser.parts)


def load_store() -> dict:
    if not DATA_FILE.exists():
        return {"notes": {}}
    try:
        value = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        return value if isinstance(value.get("notes"), dict) else {"notes": {}}
    except (OSError, json.JSONDecodeError):
        return {"notes": {}}


def save_store(value: dict) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix="notes-", suffix=".json", dir=DATA_FILE.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(value, stream, ensure_ascii=False, separators=(",", ":"))
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, DATA_FILE)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


class Handler(BaseHTTPRequestHandler):
    server_version = "H4GZenNotes/1.0"

    def send_json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def client_key(self) -> str:
        return self.headers.get("X-Forwarded-For", self.client_address[0]).split(",")[0].strip()

    def rate_limited(self) -> bool:
        now, bucket = time.monotonic(), REQUESTS[self.client_key()]
        while bucket and now - bucket[0] > WINDOW:
            bucket.popleft()
        if len(bucket) >= RATE:
            return True
        bucket.append(now)
        return False

    def send_file(self, path: Path, content_type: str) -> None:
        body = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/health":
            self.send_json(200, {"status": "ok", "editing": "public"})
        elif path == "/api/zen-notes":
            with LOCK:
                notes = load_store()["notes"]
            self.send_json(200, {"notes": notes})
        elif path in {"/zen-ctf-notes", "/zen-ctf-notes/"}:
            self.send_file(VAULT_ROOT / "zen-ctf-notes" / "index.html", "text/html; charset=utf-8")
        elif path == "/zen-ctf-notes/notes-data.js":
            self.send_file(VAULT_ROOT / "zen-ctf-notes" / "notes-data.js", "text/javascript; charset=utf-8")
        else:
            self.send_json(404, {"error": "Not found"})

    def do_PUT(self) -> None:
        path = urlparse(self.path).path
        prefix = "/api/zen-notes/"
        if not path.startswith(prefix):
            self.send_json(404, {"error": "Not found"}); return
        if self.rate_limited():
            self.send_json(429, {"error": "Rate limit exceeded. Try again shortly."}); return
        note_id = unquote(path[len(prefix):])
        try:
            if not ID_PATTERN.fullmatch(note_id) or note_id not in known_ids():
                raise ValueError("Unknown note id")
            if self.headers.get("Content-Type", "").split(";", 1)[0].strip() != "application/json":
                raise ValueError("Content-Type must be application/json")
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > MAX_BODY:
                raise ValueError(f"Request body must be between 1 and {MAX_BODY:,} bytes")
            payload = json.loads(self.rfile.read(length))
            title = str(payload.get("title", "")).strip()
            raw_html = payload.get("html", "")
            revision = int(payload.get("revision", 0))
            if not title or len(title) > 160 or not isinstance(raw_html, str):
                raise ValueError("A title up to 160 characters and HTML content are required")
            clean_html = sanitize_html(raw_html)
            if len(clean_html.encode()) > MAX_BODY:
                raise ValueError("Sanitized note is too large")
            with LOCK:
                store = load_store()
                current = store["notes"].get(note_id, {})
                current_revision = int(current.get("revision", 0))
                if revision != current_revision:
                    self.send_json(409, {"error": "This note changed since you opened it", "note": current}); return
                note = {"title": title, "html": clean_html, "revision": current_revision + 1, "updated_at": datetime.now(timezone.utc).isoformat()}
                store["notes"][note_id] = note
                save_store(store)
            self.send_json(200, {"note": note})
        except (ValueError, TypeError, json.JSONDecodeError) as error:
            self.send_json(400, {"error": str(error)})
        except Exception:
            self.send_json(500, {"error": "Unable to save note"})

    def log_message(self, fmt: str, *args) -> None:
        print(f"{self.address_string()} - {fmt % args}")


def main() -> None:
    print(f"Zen notes API listening on http://{HOST}:{PORT}")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()


if __name__ == "__main__":
    main()
