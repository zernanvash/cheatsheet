# VM AI Handoff — Enable the Protected H4G Vault

## Mission

Deploy the repository's existing vault structure behind a shared-passphrase login and HTTPS at `https://ch.zernanvash.dev`. Do not encrypt or relocate the Markdown, HTML, source mirrors, or tool directories. Do not expose a fallback static server publicly.

The authoritative runbook is [`deploy/provision-ubuntu.md`](../deploy/provision-ubuntu.md). Read it completely before changing the VM.

## What is already implemented

- `secure_server/`: FastAPI app with Argon2id login, opaque hashed SQLite sessions, ten-minute server-side leases, heartbeat-only renewal, origin checks, throttling, protected file routing, safe path resolution, and protected API proxies.
- `deploy/Caddyfile`: HTTPS reverse proxy to loopback Uvicorn with client-IP headers overwritten at the trusted hop.
- `deploy/ch-vault.service`: one Uvicorn worker bound to `127.0.0.1:8765` with systemd hardening.
- `deploy/ch-vault.env.example`: configuration names only; it intentionally contains no usable secret.
- `requirements-secure-server.txt`: pinned runtime dependencies.
- `requirements-secure-server-dev.txt`: runtime dependencies plus the pinned test runner.
- `tests/test_secure_server.py`: authentication, sessions, headers, path-policy, CSRF, source-writeup compatibility, and API-boundary tests.
- Local Marked and DOMPurify browser distributions under `assets/vendor/`; the viewer no longer needs jsDelivr and the Z3 page no longer loads Google Fonts.

## Required VM decisions and checks

1. Confirm the checkout path. The supplied service assumes `/srv/ch-vault`; adjust `WorkingDirectory` and `CH_VAULT_ROOT` together if the VM uses another absolute path.
2. Preserve the current loopback services on ports 8787–8789 for cipher identification, Zen notes, and file sharing. The secure app proxies their `/api/*` routes after authentication.
3. Check whether CyberChef is physically inside the checkout or served from a separate location. If separate, do not add a public unauthenticated Caddy route. Mount or copy it beneath the protected vault root, or extend the FastAPI server with an explicit authenticated secondary root and tests.
4. Generate the Argon2id hash interactively on the VM. Never ask the user to paste the plaintext passphrase into chat, shell history, Git, or a service file.
5. Verify Caddy owns public ports 80/443 and Uvicorn owns only `127.0.0.1:8765`.
6. Run tests, validate Caddy, and complete every acceptance check in the runbook before disabling the former public server.

## Commands after prerequisites are installed

```bash
cd /srv/ch-vault
/opt/ch-vault-venv/bin/pip install --requirement requirements-secure-server-dev.txt
/opt/ch-vault-venv/bin/pytest -q
sudo caddy validate --config /etc/caddy/Caddyfile
sudo systemctl restart ch-vault
sudo systemctl reload caddy
sudo systemctl status ch-vault caddy --no-pager
sudo ss -lntp
```

Expected repository result at handoff: the focused secure-server suite passes. If unrelated source-mirror scripts fail collection, confirm `pytest.ini` is present and do not edit `_source_*` to silence them.

## Stop conditions

Stop and report rather than improvising if:

- DNS does not resolve to this VM or a stale IPv6 record points elsewhere.
- Ports 80/443 cannot be opened or are controlled by an unknown service.
- `/etc/ch-vault/ch-vault.env` permissions cannot be restricted to root and the service group.
- The checkout or SQLite location differs and the resolved paths are uncertain.
- Caddy validation or the automated security tests fail.
- Any known vault URL is accessible without authentication after rollout.

Rollback means maintenance/closed ports, not an unauthenticated public vault.

