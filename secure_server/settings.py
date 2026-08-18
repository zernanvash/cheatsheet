"""Environment-backed configuration for the protected vault service."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from argon2 import extract_parameters
from argon2.exceptions import InvalidHashError


def _absolute_path(name: str) -> Path:
    raw = os.getenv(name, "")
    if not raw:
        raise RuntimeError(f"{name} is required")
    path = Path(raw)
    if not path.is_absolute():
        raise RuntimeError(f"{name} must be an absolute path")
    return path.resolve()


@dataclass(frozen=True)
class Settings:
    vault_root: Path
    database_path: Path
    passphrase_hash: str
    cookie_name: str = "__Host-ch_vault_session"
    session_seconds: int = 600
    origin: str = "https://ch.zernanvash.dev"
    trust_proxy: bool = True
    cipher_api: str = "http://127.0.0.1:8787"
    zen_notes_api: str = "http://127.0.0.1:8788"
    fileshare_api: str = "http://127.0.0.1:8789"

    @classmethod
    def from_env(cls) -> "Settings":
        passphrase_hash = os.getenv("CH_VAULT_PASSPHRASE_HASH", "")
        try:
            parameters = extract_parameters(passphrase_hash)
        except InvalidHashError:
            raise RuntimeError("CH_VAULT_PASSPHRASE_HASH must be an Argon2id encoded hash")
        if parameters.type.name != "ID":
            raise RuntimeError("CH_VAULT_PASSPHRASE_HASH must be an Argon2id encoded hash")
        seconds = int(os.getenv("CH_VAULT_SESSION_SECONDS", "600"))
        if seconds != 600:
            raise RuntimeError("CH_VAULT_SESSION_SECONDS must be 600 in this deployment")
        origin = os.getenv("CH_VAULT_ORIGIN", "https://ch.zernanvash.dev").rstrip("/")
        if origin != "https://ch.zernanvash.dev":
            raise RuntimeError("CH_VAULT_ORIGIN must be https://ch.zernanvash.dev")
        trust_proxy = os.getenv("CH_VAULT_TRUST_PROXY", "true").lower() == "true"
        if not trust_proxy:
            raise RuntimeError("CH_VAULT_TRUST_PROXY must be true behind loopback Caddy")
        vault_root = _absolute_path("CH_VAULT_ROOT")
        database_path = _absolute_path("CH_VAULT_DB")
        if database_path.is_relative_to(vault_root):
            raise RuntimeError("CH_VAULT_DB must be outside CH_VAULT_ROOT")
        cookie_name = os.getenv("CH_VAULT_COOKIE_NAME", "__Host-ch_vault_session")
        if not cookie_name.startswith("__Host-"):
            raise RuntimeError("CH_VAULT_COOKIE_NAME must use the __Host- prefix")
        return cls(
            vault_root=vault_root,
            database_path=database_path,
            passphrase_hash=passphrase_hash,
            cookie_name=cookie_name,
            session_seconds=seconds,
            origin=origin,
            trust_proxy=trust_proxy,
            cipher_api=os.getenv("CH_VAULT_CIPHER_API", "http://127.0.0.1:8787"),
            zen_notes_api=os.getenv("CH_VAULT_ZEN_NOTES_API", "http://127.0.0.1:8788"),
            fileshare_api=os.getenv("CH_VAULT_FILESHARE_API", "http://127.0.0.1:8789"),
        )
