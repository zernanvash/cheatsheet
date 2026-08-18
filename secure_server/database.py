"""Small SQLite session and login-throttle store."""

from __future__ import annotations

import sqlite3
import threading
import time
from pathlib import Path


class Database:
    def __init__(self, path: Path, clock=time.time) -> None:
        self.path = path
        self.clock = clock
        self.lock = threading.RLock()
        path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(path, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA journal_mode=WAL")
        self.connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS sessions (
              token_digest TEXT PRIMARY KEY,
              created_at INTEGER NOT NULL,
              last_seen_at INTEGER NOT NULL,
              expires_at INTEGER NOT NULL,
              user_agent_hash TEXT
            );
            CREATE TABLE IF NOT EXISTS login_failures (
              client_ip TEXT NOT NULL,
              failed_at INTEGER NOT NULL
            );
            CREATE INDEX IF NOT EXISTS login_failures_ip_time
              ON login_failures(client_ip, failed_at);
            """
        )

    def now(self) -> int:
        return int(self.clock())

    def cleanup(self) -> None:
        now = self.now()
        with self.lock, self.connection:
            self.connection.execute("DELETE FROM sessions WHERE expires_at <= ?", (now,))
            self.connection.execute("DELETE FROM login_failures WHERE failed_at <= ?", (now - 900,))

    def create_session(self, digest: str, seconds: int, user_agent_hash: str | None = None) -> int:
        now, expires = self.now(), self.now() + seconds
        with self.lock, self.connection:
            self.connection.execute(
                "INSERT INTO sessions VALUES (?, ?, ?, ?, ?)",
                (digest, now, now, expires, user_agent_hash),
            )
        return expires

    def session(self, digest: str):
        with self.lock:
            row = self.connection.execute(
                "SELECT * FROM sessions WHERE token_digest = ? AND expires_at > ?",
                (digest, self.now()),
            ).fetchone()
        return row

    def renew_session(self, digest: str, seconds: int) -> int | None:
        now, expires = self.now(), self.now() + seconds
        with self.lock, self.connection:
            cursor = self.connection.execute(
                "UPDATE sessions SET last_seen_at = ?, expires_at = ? "
                "WHERE token_digest = ? AND expires_at > ?",
                (now, expires, digest, now),
            )
        return expires if cursor.rowcount else None

    def delete_session(self, digest: str) -> None:
        with self.lock, self.connection:
            self.connection.execute("DELETE FROM sessions WHERE token_digest = ?", (digest,))

    def failure_count(self, client_ip: str) -> int:
        cutoff = self.now() - 900
        with self.lock:
            return int(self.connection.execute(
                "SELECT COUNT(*) FROM login_failures WHERE client_ip = ? AND failed_at > ?",
                (client_ip, cutoff),
            ).fetchone()[0])

    def record_failure(self, client_ip: str) -> int:
        with self.lock, self.connection:
            self.connection.execute(
                "INSERT INTO login_failures(client_ip, failed_at) VALUES (?, ?)",
                (client_ip, self.now()),
            )
        return self.failure_count(client_ip)

    def reset_failures(self, client_ip: str) -> None:
        with self.lock, self.connection:
            self.connection.execute("DELETE FROM login_failures WHERE client_ip = ?", (client_ip,))

