"""Passphrase and opaque session-token helpers."""

from __future__ import annotations

import hashlib
import secrets
from urllib.parse import unquote, urlsplit


def token_digest(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def new_token() -> str:
    return secrets.token_urlsafe(32)


def user_agent_digest(value: str) -> str | None:
    return hashlib.sha256(value.encode()).hexdigest()[:16] if value else None


def safe_next(value: str | None) -> str:
    if not value or not value.startswith("/") or value.startswith("//"):
        return "/"
    decoded = unquote(value)
    if "\\" in decoded or any(ord(char) < 32 or ord(char) == 127 for char in decoded):
        return "/"
    parsed = urlsplit(value)
    return value if not parsed.scheme and not parsed.netloc else "/"
