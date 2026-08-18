from __future__ import annotations

from pathlib import Path

import pytest
from argon2 import PasswordHasher
from fastapi.testclient import TestClient

from secure_server.app import SECURITY_HEADERS, create_app
from secure_server.auth import safe_next, token_digest
from secure_server.paths import PathDenied, resolve_vault_path
from secure_server.settings import Settings


class Clock:
    def __init__(self, value=1_800_000_000):
        self.value = value

    def __call__(self):
        return self.value


@pytest.fixture
def vault(tmp_path: Path):
    (tmp_path / "index.html").write_text("<html><head></head><body>home</body></html>", encoding="utf-8")
    (tmp_path / "page.md").write_text("# private", encoding="utf-8")
    (tmp_path / "writeups-index.json").write_text("[]", encoding="utf-8")
    (tmp_path / "assets").mkdir()
    (tmp_path / "assets" / "app.js").write_text("window.ok=true", encoding="utf-8")
    source = tmp_path / "_source_example"
    source.mkdir()
    (source / "writeup.md").write_text("# source", encoding="utf-8")
    return tmp_path


@pytest.fixture
def setup(vault: Path, tmp_path: Path):
    clock = Clock()
    settings = Settings(
        vault_root=vault,
        database_path=tmp_path / "security.db",
        passphrase_hash=PasswordHasher(time_cost=1, memory_cost=8192).hash("correct horse"),
    )
    app = create_app(settings, clock=clock, delay=lambda _seconds: _no_delay())
    with TestClient(app, base_url="https://ch.zernanvash.dev") as client:
        yield client, app.state.database, clock, settings


async def _no_delay():
    return None


def login(client: TestClient, passphrase="correct horse", next_path="/"):
    return client.post(
        "/auth/login",
        data={"passphrase": passphrase, "next": next_path},
        headers={"Origin": "https://ch.zernanvash.dev"},
        follow_redirects=False,
    )


def test_anonymous_existing_and_missing_files_are_indistinguishable(setup):
    client, *_ = setup
    existing = client.get("/page.md", follow_redirects=False)
    missing = client.get("/does-not-exist.md", follow_redirects=False)
    assert (existing.status_code, existing.headers["location"].split("?", 1)[0]) == (303, "/login")
    assert (missing.status_code, missing.headers["location"].split("?", 1)[0]) == (303, "/login")
    assert "private" not in existing.text + missing.text


def test_login_creates_hashed_server_session_and_secure_cookie(setup):
    client, database, *_ = setup
    response = login(client)
    assert response.status_code == 303
    cookie = response.headers["set-cookie"]
    assert "Secure" in cookie and "HttpOnly" in cookie and "SameSite=strict" in cookie
    assert "Domain=" not in cookie and "Max-Age=600" in cookie
    raw = client.cookies.get("__Host-ch_vault_session")
    assert database.session(token_digest(raw)) is not None
    assert raw not in database.connection.execute("SELECT token_digest FROM sessions").fetchone()[0]


def test_bad_login_is_generic_and_does_not_create_session(setup):
    client, database, *_ = setup
    response = login(client, "wrong")
    assert response.status_code == 401
    assert "Invalid passphrase or login temporarily unavailable." in response.text
    assert database.connection.execute("SELECT COUNT(*) FROM sessions").fetchone()[0] == 0


def test_login_throttle_threshold_and_successful_reset(setup):
    client, database, *_ = setup
    for _ in range(10):
        assert login(client, "wrong").status_code == 401
    blocked = login(client, "wrong")
    assert blocked.status_code == 429
    assert blocked.headers["retry-after"] == "900"
    database.reset_failures("testclient")
    assert login(client).status_code == 303
    assert database.failure_count("testclient") == 0


def test_login_rotates_existing_session(setup):
    client, database, *_ = setup
    assert login(client).status_code == 303
    old = client.cookies.get("__Host-ch_vault_session")
    assert login(client).status_code == 303
    new = client.cookies.get("__Host-ch_vault_session")
    assert new != old
    assert database.session(token_digest(old)) is None
    assert database.session(token_digest(new)) is not None


def test_status_does_not_renew_but_heartbeat_does(setup):
    client, database, clock, settings = setup
    login(client)
    raw = client.cookies.get(settings.cookie_name)
    initial = database.session(token_digest(raw))["expires_at"]
    clock.value += 100
    status = client.get("/auth/status")
    assert status.json()["expires_at"] == initial
    assert client.get("/page.md").status_code == 200
    assert database.session(token_digest(raw))["expires_at"] == initial
    heartbeat = client.post("/auth/heartbeat", headers={"Origin": settings.origin})
    assert heartbeat.status_code == 200
    assert heartbeat.json()["expires_at"] == clock.value + 600


def test_expired_and_forged_tokens_fail(setup):
    client, _, clock, settings = setup
    login(client)
    clock.value += 601
    assert client.get("/auth/status").status_code == 401
    client.cookies.set(settings.cookie_name, "forged-token-that-is-long-enough")
    assert client.get("/auth/status").status_code == 401


def test_logout_requires_origin_and_deletes_session(setup):
    client, database, _, settings = setup
    login(client)
    raw = client.cookies.get(settings.cookie_name)
    assert client.post("/auth/logout", headers={"Origin": "https://evil.example"}).status_code == 403
    response = client.post("/auth/logout", headers={"Origin": settings.origin})
    assert response.status_code == 204
    assert database.session(token_digest(raw)) is None


def test_authenticated_files_source_writeups_and_headers(setup):
    client, *_ = setup
    login(client)
    home = client.get("/")
    assert home.status_code == 200
    assert '/_auth/session-lease.js' in home.text
    assert client.get("/_source_example/writeup.md").status_code == 200
    assert client.get("/writeups-index.json").headers["cache-control"] == "no-store"
    for name, value in SECURITY_HEADERS.items():
        assert home.headers[name] == value
    assert "Content-Security-Policy" in home.headers


@pytest.mark.parametrize("path", [
    b"/../index.html", b"/%2e%2e/index.html", b"/assets%5capp.js", b"/%00index.html",
    b"/.git/config", b"/.agents/plan.md", b"/secure_server/app.py", b"/secret.env",
])
def test_path_policy_denies_traversal_and_operational_files(vault, path):
    with pytest.raises((PathDenied, FileNotFoundError)):
        resolve_vault_path(vault, path)


def test_symlink_escape_is_denied(vault, tmp_path):
    outside = tmp_path.parent / "outside.md"
    outside.write_text("outside", encoding="utf-8")
    link = vault / "link.md"
    try:
        link.symlink_to(outside)
    except OSError:
        pytest.skip("symlinks unavailable")
    with pytest.raises(PathDenied):
        resolve_vault_path(vault, b"/link.md")


@pytest.mark.parametrize("value", ["https://evil.example", "//evil.example", "/ok\nSet-Cookie:x", "/%0d%0aHeader:x", "/%5cevil.example", None])
def test_open_redirects_are_rejected(value):
    assert safe_next(value) == "/"


def test_api_requires_authentication(setup):
    client, *_ = setup
    assert client.get("/api/fileshare").status_code == 401
    assert client.post("/api/cipher-identify", json={"text": "abc"}).status_code == 401
