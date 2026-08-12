# Deploy the Cipher Identifier on Ubuntu

The public page is `https://ch.zernanvash.dev/cipher-identifier/`. Nginx serves the static directory and proxies only `POST /api/cipher-identify` to a Python service bound to localhost.

## 1. Deploy the vault

```bash
sudo install -d -o www-data -g www-data /var/www/h4g
sudo git -C /var/www/h4g pull --ff-only origin main
```

Adjust this step if the existing site deploy uses a different checkout path.

## 2. Install and configure OpenCode

Install OpenCode using its official method, create a locked service account, authenticate its provider, and confirm headless output:

```bash
sudo useradd --system --home /var/lib/h4g-cipher --create-home --shell /usr/sbin/nologin h4g-cipher
sudo -u h4g-cipher env HOME=/var/lib/h4g-cipher XDG_CONFIG_HOME=/var/lib/h4g-cipher/config opencode auth login
sudo -u h4g-cipher env HOME=/var/lib/h4g-cipher XDG_CONFIG_HOME=/var/lib/h4g-cipher/config opencode run --format json 'Return only: {"ok":true}'
```

The identifier invokes `opencode run --format json` with a short timeout. Set the exact binary and optional model in `/etc/h4g-cipher-identifier.env`:

```bash
sudo install -m 600 -o root -g root deploy/cipher-identifier.env.example /etc/h4g-cipher-identifier.env
sudoedit /etc/h4g-cipher-identifier.env
```

Set `CIPHER_AI_ENABLED=0` for algorithm-only operation. The page and API remain functional.

## 3. Install the systemd unit

```bash
sudo install -m 644 deploy/cipher-identifier.service /etc/systemd/system/cipher-identifier.service
sudo systemctl daemon-reload
sudo systemctl enable --now cipher-identifier.service
curl http://127.0.0.1:8787/health
```

The unit stores the service account's OpenCode configuration under `/var/lib/h4g-cipher/config`; credentials never belong in the web root.

## 4. Configure Nginx

Copy the locations from `deploy/nginx-cipher-identifier.conf` into the existing HTTPS `server` block for `ch.zernanvash.dev`, then validate and reload:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

The existing static root must point to `/var/www/h4g` (or its deployed equivalent) so `/cipher-identifier/` resolves `cipher-identifier/index.html`.

## 5. Verify

```bash
curl -sS https://ch.zernanvash.dev/api/cipher-identify \
  -H 'Content-Type: application/json' \
  --data '{"text":"SGVsbG8gd29ybGQ=","use_ai":false}'

sudo journalctl -u cipher-identifier.service -n 100 --no-pager
```

Expected algorithmic top match: `base64`. Enable AI only after the deterministic endpoint passes.

## Trust boundary

- The classifier ranks a fixed allowlist from computed features.
- OpenCode sees a maximum 2,000-character sample plus the top five candidates.
- AI output must be valid JSON and may reference only those candidate IDs.
- Invalid, timed-out, or unavailable AI output is discarded.
- The API returns deterministic candidates even when AI is disabled or fails.
- Nginx limits request bodies; the Python service also enforces size and per-IP rate limits.
