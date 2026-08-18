"""Safe import-time defaults for secure-server tests."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

from argon2 import PasswordHasher


_temp = Path(tempfile.mkdtemp(prefix="ch-vault-tests-"))
_db_temp = Path(tempfile.mkdtemp(prefix="ch-vault-db-tests-"))
(_temp / "index.html").write_text("<html><head></head><body>test</body></html>", encoding="utf-8")
os.environ.setdefault("CH_VAULT_ROOT", str(_temp.resolve()))
os.environ.setdefault("CH_VAULT_DB", str((_db_temp / "import.db").resolve()))
os.environ.setdefault("CH_VAULT_PASSPHRASE_HASH", PasswordHasher(time_cost=1, memory_cost=8192).hash("import-only"))
os.environ.setdefault("CH_VAULT_SESSION_SECONDS", "600")
os.environ.setdefault("CH_VAULT_ORIGIN", "https://ch.zernanvash.dev")
os.environ.setdefault("CH_VAULT_TRUST_PROXY", "true")
