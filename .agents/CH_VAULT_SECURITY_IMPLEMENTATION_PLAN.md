# `ch.zernanvash.dev` Authenticated HTTPS Vault — Implementation Handoff

## 1. Outcome and security boundary

Replace the Azure VM's unauthenticated static-file server with an HTTPS-only, server-authenticated deployment for the H4G vault at `https://ch.zernanvash.dev`.

The finished deployment must:

- Require one shared passphrase before any vault HTML, Markdown, JSON, JavaScript, CSS, image, download, or API response is returned.
- Keep access alive while at least one authenticated vault tab remains open by renewing a server-side lease.
- Allow the browser to be reopened without another prompt for up to 10 minutes after the final successful heartbeat.
- Require the passphrase again after that lease expires.
- Encrypt HTTP payloads in transit with TLS. A passive packet capture must not reveal the passphrase, cookie, requested URL path, query string, Markdown, JSON, or response body.
- Make no promise of anonymity: DNS/domain, Azure IP, TCP/TLS connection timing, and approximate byte counts remain observable.

This is access control plus transport encryption. Do not add custom payload ciphers, JavaScript-only password gates, URL obfuscation, VPN dependencies, traffic morphing, or home-grown cryptography.

## 2. Fixed architecture

Use this stack without substituting components:

- Ubuntu Azure VM.
- Caddy as the public reverse proxy and TLS terminator.
- Python 3.12 virtual environment.
- FastAPI application served by Uvicorn with exactly one worker.
- Argon2id through `argon2-cffi` for the shared passphrase hash.
- SQLite for hashed session tokens and login-throttle state.
- `systemd` services for Caddy and the application.

Request flow:

```text
Browser
  -> HTTPS :443 at ch.zernanvash.dev
  -> Caddy
  -> HTTP 127.0.0.1:8765
  -> FastAPI authentication and authorization
  -> approved vault file or auth response
```

Caddy must be the only process listening publicly. The FastAPI service must bind to `127.0.0.1:8765`, never `0.0.0.0`.

## 3. Repository additions and edits

Create the following implementation:

```text
secure_server/
├── __init__.py
├── app.py                 # FastAPI construction, middleware, routes, file serving
├── auth.py                # passphrase verification, token hashing, cookie helpers
├── database.py            # SQLite schema, transactions, cleanup
├── paths.py               # canonicalization and approved/denied path policy
├── settings.py            # validated environment configuration
├── static/
│   ├── login.css
│   └── session-lease.js   # tab coordination and heartbeat client
└── templates/
    └── login.html
tests/
├── test_auth.py
├── test_file_policy.py
├── test_headers.py
└── test_sessions.py
deploy/
├── Caddyfile
├── ch-vault.service
├── ch-vault.env.example
└── provision-ubuntu.md
requirements-secure-server.txt
```

Also edit:

- `assets/vault-ui.js` to load the session-lease client on authenticated pages, or incorporate the lease code directly there. Use only one implementation, not both.
- `viewer.html` to replace jsDelivr references to Marked and DOMPurify with locally vendored copies under `assets/vendor/`.
- `rev_source/z3_practice.html` to remove Google Fonts requests and use a local font or the existing system-font stack.
- Every other runtime `http://` or `https://` asset include to eliminate third-party requests. Ordinary user-clicked reference links may remain.
- `README.md` with separate local-development and protected Azure deployment instructions. State clearly that `python -m http.server` is local-only and must not be used for the public deployment.
- `.gitignore` to exclude the SQLite database, environment files, virtual environments, Python caches, and temporary session data.

Do not modify `.obsidian/`, restructure `_source_*`, manually edit `writeups-index.json`, or remove existing vault content.

## 4. Configuration contract

`secure_server/settings.py` must load and validate these environment variables at startup:

| Variable | Required value or behavior |
| --- | --- |
| `CH_VAULT_ROOT` | Absolute repository root used for approved file resolution. |
| `CH_VAULT_DB` | Absolute SQLite path outside the Git working tree, recommended `/var/lib/ch-vault/security.db`. |
| `CH_VAULT_PASSPHRASE_HASH` | Argon2id encoded hash; fail startup if absent or malformed. |
| `CH_VAULT_COOKIE_NAME` | Default `__Host-ch_vault_session`. |
| `CH_VAULT_SESSION_SECONDS` | Fixed production value `600`. |
| `CH_VAULT_ORIGIN` | Exact value `https://ch.zernanvash.dev`. |
| `CH_VAULT_TRUST_PROXY` | Fixed value `true`; accept forwarding data only from the loopback Caddy hop. |

Never accept a plaintext passphrase through configuration. Include a documented one-time command that reads a passphrase without echoing it and prints an Argon2id hash for the administrator to place in `/etc/ch-vault/ch-vault.env`. Do not write the plaintext or generated hash into Git.

The production environment file must be owned by root, readable by the service group only, and mode `0640`. The SQLite directory must be writable only by the service account.

## 5. Authentication and session behavior

### Login

Implement:

- `GET /login`: return the locally styled passphrase form. If already authenticated, redirect to `/`.
- `POST /auth/login`: accept `application/x-www-form-urlencoded` with only `passphrase` and `next`.
- Restrict `next` to a normalized same-origin path beginning with `/`; fall back to `/` for invalid, absolute, scheme-relative, or control-character-containing values.
- Verify the submitted passphrase with Argon2id. Use the library's normal verifier and handle mismatch/malformed-hash errors without exposing which condition occurred.
- On success, create a 32-byte token with `secrets.token_urlsafe(32)`, store only its SHA-256 digest in SQLite, and return the raw token only in the cookie.
- On success, rotate away any existing session token supplied by the browser.
- On failure, return the same generic message and response shape for all invalid credentials.

### Cookie

Set exactly one authentication cookie:

```text
Name: __Host-ch_vault_session
Path: /
Secure: true
HttpOnly: true
SameSite: Strict
Max-Age: 600
Domain: omitted
```

Refresh `Max-Age=600` only after a valid heartbeat. Clear it with the same path and security attributes on logout or when an expired/unknown token is encountered.

### Server-side session record

Store:

- `token_digest` as the primary key.
- `created_at` as UTC epoch seconds.
- `last_seen_at` as UTC epoch seconds.
- `expires_at` as UTC epoch seconds.
- Optional truncated user-agent hash for anomaly logging only; never make it an authentication requirement.

A session is valid only when its digest exists and `expires_at > current_server_time`. Do not trust cookie expiry as authorization. Update `last_seen_at` and `expires_at = now + 600` atomically during heartbeat. Delete expired sessions opportunistically on login/heartbeat and through a periodic cleanup task.

### Open-tab lease

Implement these browser semantics:

- `POST /auth/heartbeat` is the only endpoint that renews the 10-minute lease. Normal file requests do not extend it.
- Start a heartbeat immediately after an authenticated page loads, then every 120 seconds.
- Use `BroadcastChannel('ch-vault-session')` plus a localStorage leader lease so normally only one tab sends heartbeats.
- Renew the leader lease every 30 seconds and allow another tab to take over if it has not been renewed for 75 seconds.
- When a tab becomes visible or receives focus, check leadership and send an immediate heartbeat if the last successful heartbeat is older than 120 seconds.
- Treat `401` as session expiry: stop timers and navigate to `/login?next=<current same-origin path>`.
- Closing the last tab stops heartbeats. Browser unload events are not relied upon for logout.
- Reopening within 10 minutes works because the persistent cookie and server record are still valid. Reopening later fails server validation and returns to login.

### Logout and status

- `POST /auth/logout`: require a valid same-origin request, delete the supplied session record if present, clear the cookie, and return `204`.
- `GET /auth/status`: return `200 {"authenticated":true,"expires_at":...}` for a valid lease and `401 {"authenticated":false}` otherwise. It must not renew the lease.

## 6. CSRF, origin, and brute-force controls

For every state-changing endpoint:

- Require `Origin: https://ch.zernanvash.dev`.
- If `Origin` is absent, require `Sec-Fetch-Site: same-origin`; otherwise reject with `403`.
- Accept only the documented HTTP method and content type.
- Rely on the host-only `SameSite=Strict` cookie plus origin validation; do not expose a bearer token to JavaScript.

Throttle failed login attempts by the immediate Caddy-provided client IP:

- First 5 failures in 15 minutes: normal response.
- Failures 6–10: enforce a two-second server-side delay.
- More than 10: return `429` with `Retry-After: 900` until the 15-minute window expires.
- Reset the failure counter after a successful login.
- Do not trust arbitrary `X-Forwarded-For` values. Caddy must overwrite forwarding headers, and the application must only honor them because the socket peer is loopback.

Use a generic login error and do not log submitted passphrases.

## 7. Protected-file policy

All vault content, including `/`, is private. Authentication must run before file existence is disclosed.

Normalize file requests as follows:

1. Percent-decode once and reject malformed encoding or NUL/control characters.
2. Convert URL separators consistently and reject backslashes.
3. Resolve the requested path against `CH_VAULT_ROOT` with `Path.resolve(strict=True)`.
4. Require the resolved path to remain beneath the resolved vault root.
5. Reject symlinks whose final resolved target leaves the root.
6. Map `/` to `/index.html` and directory paths to their `index.html` only when present.

Deny before checking extensions if any path component:

- Starts with `.`.
- Starts with `_source_`.
- Equals `.git`, `.agents`, `.obsidian`, `.playwright-cli`, `secure_server`, `tests`, `deploy`, `scripts`, `node_modules`, `__pycache__`, or a virtual-environment directory.
- Is a known runtime/log directory.

Deny filenames matching secrets or operational artifacts, including `*.env`, `*.db`, `*.sqlite*`, `*.log`, `*.pem`, `*.key`, service files, Caddy configuration, requirements files, Python source, PowerShell, batch, and shell scripts. `install.sh` must not be served by the protected vault unless a later explicit requirement adds a narrowly scoped route.

Allow only the extensions currently required by the viewer after inventorying reachable links, with this baseline:

```text
.html .htm .css .js .json .md .txt
.png .jpg .jpeg .gif .webp .svg .ico
.woff .woff2
.pdf .zip
```

Do not automatically broaden the allowlist when a request fails. Inventory the legitimate reference first and add the minimum extension with a regression test.

Use framework/file-response MIME detection with explicit safe overrides. Set `Content-Disposition: attachment` for archive/binary downloads and `X-Content-Type-Options: nosniff` globally.

## 8. Response headers and caching

Set these headers on application responses; Caddy may set HSTS at the edge but there must be one authoritative configuration:

```text
Strict-Transport-Security: max-age=31536000; includeSubDomains
Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self'; frame-ancestors 'none'
X-Content-Type-Options: nosniff
Referrer-Policy: no-referrer
Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=()
Cross-Origin-Opener-Policy: same-origin
```

Use `Cache-Control: no-store` for `/login`, all `/auth/*` responses, Markdown, JSON indexes, and HTML. Static CSS/JS/images may use private browser caching with validators, but never `public` shared-cache directives.

Do not enable HSTS preload. `includeSubDomains` is accepted because the selected hostname is already a subdomain and the administrator controls `zernanvash.dev`; if another subdomain cannot support HTTPS, remove only that directive before deployment and document the reason.

## 9. Local dependencies and privacy

The browser must not contact third parties merely to render the vault:

- Vendor pinned Marked and DOMPurify distributions under `assets/vendor/` and document their upstream versions and licenses.
- Replace Google Fonts with system fonts or locally stored font files.
- Scan HTML, CSS, and JavaScript for remote `src`, stylesheet, font, `fetch`, WebSocket, and preconnect targets.
- Keep ordinary external hyperlinks usable only after an explicit user click.
- Confirm the CSP reports no blocked dependency required for normal operation.

Do not fetch third-party JavaScript at runtime and do not loosen CSP to make an external dependency work.

## 10. Caddy and DNS deployment

Before certificate issuance:

- Confirm the public DNS `A` record for `ch.zernanvash.dev` points to the Azure VM public IPv4 address.
- Remove a stale `AAAA` record unless the VM has functioning public IPv6.
- If the record is managed through Cloudflare, set it to DNS-only for the initial direct-Caddy deployment. Do not leave an unplanned CDN proxy in front of the origin.
- Confirm Azure NSG and Ubuntu firewall allow inbound TCP 80 and 443.

`deploy/Caddyfile` must use:

```caddyfile
ch.zernanvash.dev {
    encode zstd gzip
    reverse_proxy 127.0.0.1:8765
}
```

Do not enable full request access logs in the initial configuration. Caddy service/error logs may remain in journald with normal retention, but must not contain cookies, authorization values, request bodies, or passphrases.

Caddy will use port 80 for ACME/redirect handling and port 443 for TLS. Verify automatic certificate renewal with `caddy validate`, service status, and Caddy logs.

## 11. systemd deployment

Create a dedicated unprivileged `ch-vault` system user with no interactive shell. The service must:

- Use the repository checkout as read-only application content from the service's perspective where practical.
- Read `/etc/ch-vault/ch-vault.env` through `EnvironmentFile=`.
- Run `/opt/ch-vault-venv/bin/uvicorn secure_server.app:app --host 127.0.0.1 --port 8765 --workers 1`.
- Use `Restart=on-failure` and a short restart delay.
- Set `NoNewPrivileges=true`, `PrivateTmp=true`, `ProtectSystem=strict`, `ProtectHome=true`, and grant write access only to `/var/lib/ch-vault`.
- Start after the network is online and before/independently of Caddy.

Document exact provisioning, ownership, permission, service-enable, service-restart, validation, and rollback commands in `deploy/provision-ubuntu.md`. Never place the live passphrase hash, VM IP, SSH key, or other secret in that document.

## 12. Tests and acceptance criteria

Use `pytest`, FastAPI's test client, and temporary roots/databases. Freeze or inject time for expiry tests; do not make the suite sleep for minutes.

Required automated tests:

- Correct passphrase creates a server record and correctly attributed cookie.
- Incorrect passphrase never creates a session and returns only the generic error.
- Rate-limit thresholds, delays through a mockable delay function, reset, and `Retry-After` behavior.
- Existing token is revoked when login rotates it.
- Valid, expired, deleted, malformed, and randomly forged tokens.
- Heartbeat extends both server expiry and cookie expiry; ordinary file/status requests do not.
- Logout deletes the record and clears the cookie.
- Origin/Sec-Fetch enforcement for all state-changing routes.
- Anonymous requests cannot distinguish a missing protected file from an existing one through response body or redirect behavior.
- Direct access to `writeups-index.json`, `search-index.json`, Markdown, raw links, images, and nested HTML requires authentication.
- Traversal using `..`, percent encoding, double encoding, backslashes, NULs, alternate separators, symlinks, and mixed case is denied.
- Every denied directory, secret suffix, and operational file class is denied.
- Legitimate reachable vault assets are served with correct MIME type.
- Required security and cache headers appear on success, redirect, client error, and server error responses.
- Open redirects through `next` are rejected.

Required browser/deployment checks:

1. Visit `http://ch.zernanvash.dev`; confirm redirect to HTTPS.
2. Confirm a valid browser-trusted certificate for exactly `ch.zernanvash.dev`.
3. Before login, directly request known JSON/Markdown/image URLs and confirm no content disclosure.
4. Login, browse all primary entry points, use search, open raw Markdown, and exercise the Z3 page.
5. Open several tabs and confirm only one normal heartbeat stream in developer tools.
6. Close every tab, reopen within 10 minutes, and confirm access remains.
7. Close every tab, wait more than 10 minutes after the final heartbeat, reopen, and confirm login is required.
8. Leave one tab open for more than 10 minutes and confirm heartbeats retain access despite the original login time.
9. Restart the app. Existing SQLite-backed unexpired sessions should remain valid; if the implementation intentionally purges sessions on startup instead, change this requirement and document the operational tradeoff before coding. The selected default is persistence across routine service restarts.
10. Use browser developer tools to verify cookie attributes, response headers, no mixed content, and no automatic third-party requests.
11. Capture traffic from a separate test client and verify the packet capture cannot read credentials, cookie values, HTTP paths/query strings, or payload content. Record that IP/domain timing and byte volume remain visible.

The implementation is accepted only when all automated tests pass, Caddy and the app survive a VM reboot, the public origin exposes no unauthenticated vault content, and the browser makes no required third-party runtime requests.

## 13. Rollout and rollback

Roll out in this order:

1. Implement and pass tests locally using temporary configuration.
2. Inventory and vendor remote runtime dependencies.
3. Provision the service account, venv, environment hash, and database directory on the VM.
4. Start FastAPI on loopback and validate it locally with Caddy stopped or using a local Host header.
5. Validate the Caddyfile and DNS.
6. Start Caddy and test HTTPS plus authentication from a separate device.
7. Remove/disable the old public `python -m http.server` or any other service exposing the repository.
8. Reboot the VM and repeat the smoke tests.

Rollback must stop/disable `ch-vault` and restore the previous known-good web service configuration. Do not roll back to an unauthenticated service on a public interface; if authentication deployment fails, serve a maintenance response or close ports 80/443 until fixed.

## 14. Explicit assumptions

- `ch.zernanvash.dev` is intended for a small authorized group but remains reachable over the public internet.
- One shared passphrase is deliberate. It prevents individual attribution and individual revocation; rotating it affects every user.
- The administrator distributes the generated passphrase through a separate trusted channel.
- TLS terminates directly on the Azure VM through Caddy; no VPN or CDN is part of this version.
- The vault remains read-only through this service except for separately existing APIs, which must independently pass the same authentication/origin controls before exposure.
- SQLite and a single Uvicorn worker are sufficient for the small group. Do not add Redis or a multi-node session system.
- Transport confidentiality, robust authentication, and minimized third-party leakage are the goals. Hiding that communication with the Azure host occurred is not achievable and is outside scope.
