"""Canonical vault-path resolution and publication policy."""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote_to_bytes


ALLOWED_EXTENSIONS = {
    ".html", ".htm", ".css", ".js", ".json", ".md", ".txt", ".csv",
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".ico",
    ".woff", ".woff2", ".pdf", ".zip", ".docx", ".wasm", ".gz", ".map",
}
DENIED_COMPONENTS = {
    ".git", ".agents", ".obsidian", ".playwright-cli", ".codex",
    "secure_server", "tests", "deploy", "scripts", "node_modules", "__pycache__",
    ".venv", "venv", "env",
}
DENIED_SUFFIXES = {
    ".env", ".db", ".sqlite", ".sqlite3", ".log", ".pem", ".key",
    ".service", ".conf", ".py", ".pyc", ".ps1", ".bat", ".cmd", ".sh",
    ".exe", ".dll", ".sys", ".bin",
}
MALFORMED_PERCENT = re.compile(r"%(?![0-9a-fA-F]{2})")


class PathDenied(Exception):
    pass


def decode_raw_path(raw_path: bytes) -> str:
    raw = raw_path.decode("ascii", "strict")
    if MALFORMED_PERCENT.search(raw):
        raise PathDenied
    try:
        value = unquote_to_bytes(raw).decode("utf-8", "strict")
    except (UnicodeDecodeError, ValueError):
        raise PathDenied from None
    if "\\" in value or any(ord(char) < 32 or ord(char) == 127 for char in value):
        raise PathDenied
    return value


def resolve_vault_path(root: Path, raw_path: bytes) -> Path:
    requested = decode_raw_path(raw_path).lstrip("/") or "index.html"
    components = [part for part in requested.split("/") if part]
    folded = [part.casefold() for part in components]
    if any(part in {".", ".."} for part in components):
        raise PathDenied
    if any(part.startswith(".") for part in components):
        raise PathDenied
    if any(part in DENIED_COMPONENTS for part in folded):
        raise PathDenied

    candidate = (root / Path(*components)).resolve(strict=True)
    resolved_root = root.resolve(strict=True)
    if not candidate.is_relative_to(resolved_root):
        raise PathDenied
    if candidate.is_dir():
        candidate = (candidate / "index.html").resolve(strict=True)
        if not candidate.is_relative_to(resolved_root):
            raise PathDenied

    suffix = candidate.suffix.casefold()
    name = candidate.name.casefold()
    if suffix in DENIED_SUFFIXES or name.endswith(".env.example") or suffix not in ALLOWED_EXTENSIONS:
        raise PathDenied
    return candidate
