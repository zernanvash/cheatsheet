# Protected Vault Deployment on Ubuntu

This handout is written for the AI or administrator operating the Ubuntu VM. It deploys access control and HTTPS without changing or encrypting the vault's content structure.

## Safety boundary

- Run the application only on `127.0.0.1:8765`.
- Caddy is the only public listener and owns ports 80/443.
- Never commit `/etc/ch-vault/ch-vault.env`, the generated Argon2id hash, or `/var/lib/ch-vault/security.db`.
- Do not restore `python -m http.server` on a public interface during rollback.
- Existing cipher identifier, Zen notes, and file-share services stay on loopback. Their `/api/*` routes are reached through the authenticated vault server.

## 1. Preflight

The checkout is `/var/www/ch.zernanvash.dev`. Confirm DNS points to this VM, no stale `AAAA` record exists without working IPv6, and TCP 80/443 are allowed by the Azure NSG and Ubuntu firewall.

```bash
cd /var/www/ch.zernanvash.dev
git status --short --branch
python3 --version
getent ahostsv4 ch.zernanvash.dev
sudo ss -lntp
```

The service expects Python 3.12. Install Caddy from its official Ubuntu repository and ensure no old web server is occupying ports 80/443.

## 2. Service account and virtual environment

```bash
sudo useradd --system --home-dir /nonexistent --shell /usr/sbin/nologin ch-vault
sudo python3 -m venv /opt/ch-vault-venv
sudo /opt/ch-vault-venv/bin/pip install --requirement /var/www/ch.zernanvash.dev/requirements-secure-server-dev.txt
sudo install -d -o root -g ch-vault -m 0750 /etc/ch-vault
sudo install -d -o ch-vault -g ch-vault -m 0750 /var/lib/ch-vault
```

Give `ch-vault` read/execute access to the checkout. Do not give it Git credentials or write access to repository content.

## 3. Generate the passphrase hash

This reads the passphrase without echo and prints only its Argon2id hash:

```bash
sudo /opt/ch-vault-venv/bin/python -c 'from getpass import getpass; from argon2 import PasswordHasher; print(PasswordHasher().hash(getpass("Vault passphrase: ")))' 
```

Copy the example, place the generated hash after `CH_VAULT_PASSPHRASE_HASH=`, and protect the file:

```bash
sudo install -m 0640 -o root -g ch-vault /var/www/ch.zernanvash.dev/deploy/ch-vault.env.example /etc/ch-vault/ch-vault.env
sudoedit /etc/ch-vault/ch-vault.env
sudo stat -c '%U %G %a %n' /etc/ch-vault/ch-vault.env /var/lib/ch-vault
```

## 4. Install and start the application

```bash
sudo install -m 0644 /var/www/ch.zernanvash.dev/deploy/ch-vault.service /etc/systemd/system/ch-vault.service
sudo systemctl daemon-reload
sudo systemctl enable --now ch-vault
sudo systemctl status ch-vault --no-pager
sudo journalctl -u ch-vault -n 100 --no-pager
curl --include --header 'Host: ch.zernanvash.dev' http://127.0.0.1:8765/login
```

Expected: the app listens only on loopback and `/login` returns HTML with security headers.

## 5. Install Caddy configuration

Back up the current Caddyfile before replacing it. Validate before reload:

```bash
sudo cp /etc/caddy/Caddyfile /etc/caddy/Caddyfile.pre-ch-vault
sudo install -m 0644 /var/www/ch.zernanvash.dev/deploy/Caddyfile /etc/caddy/Caddyfile
sudo caddy validate --config /etc/caddy/Caddyfile
sudo systemctl reload caddy
sudo systemctl status caddy --no-pager
sudo journalctl -u caddy -n 100 --no-pager
```

Disable the former public static server only after the loopback application and Caddy configuration both validate.

## 6. Acceptance checks

From a separate device:

1. Confirm HTTP redirects to HTTPS and the certificate is trusted for `ch.zernanvash.dev`.
2. Request `/`, `/writeups-index.json`, and a known Markdown URL before login; all must redirect to the same login flow without content disclosure.
3. Log in, browse the home page, viewer, writeup search, Z3 practice, cipher tools, Zen notes, and file sharing.
4. Verify the cookie is `Secure`, `HttpOnly`, `SameSite=Strict`, host-only, `Path=/`, and has a 600-second lifetime.
5. Confirm developer tools show no automatic requests to jsDelivr or Google Fonts.
6. Open several tabs. Normally one tab should send `/auth/heartbeat` every two minutes. Close all tabs: reopening inside ten minutes works; reopening after the lease expires requires login.
7. Confirm `/api/cipher-identify`, `/api/zen-notes`, and `/api/fileshare` return `401` without the session.
8. Reboot and repeat login, browsing, and `systemctl status` checks.

Run the repository test suite before deployment:

```bash
cd /var/www/ch.zernanvash.dev
/opt/ch-vault-venv/bin/pytest -q
```

## Updating

```bash
cd /var/www/ch.zernanvash.dev
git pull --ff-only origin main
sudo /opt/ch-vault-venv/bin/pip install --requirement requirements-secure-server.txt
sudo systemctl restart ch-vault
sudo caddy validate --config /etc/caddy/Caddyfile
```

Do not overwrite the live environment file or database during an update.

## Rollback

If authentication deployment fails, keep the origin closed or serve maintenance content. Do not expose the vault unauthenticated.

```bash
sudo systemctl disable --now ch-vault
sudo cp /etc/caddy/Caddyfile.pre-ch-vault /etc/caddy/Caddyfile
sudo caddy validate --config /etc/caddy/Caddyfile
sudo systemctl reload caddy
```

If the previous Caddyfile exposed the vault publicly, do not restore it; stop Caddy until the authenticated service is repaired.
