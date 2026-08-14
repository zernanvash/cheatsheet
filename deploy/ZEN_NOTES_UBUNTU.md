# Deploy the public Zen CTF Notes editor

The editor is deliberately unauthenticated: anyone who can open `https://ch.zernanvash.dev/zen-ctf-notes/` can change its shared notes. Saved overrides live outside the Git checkout at `/var/lib/h4g-zen-notes/notes.json`, so `git pull` does not erase community edits.

## Install the service

```bash
sudo useradd --system --home /var/lib/h4g-zen-notes --create-home --shell /usr/sbin/nologin h4g-zen-notes
sudo install -m 644 deploy/zen-notes.service /etc/systemd/system/zen-notes.service
sudo systemctl daemon-reload
sudo systemctl enable --now zen-notes.service
curl http://127.0.0.1:8788/health
```

## Configure Nginx

Copy the two locations from `deploy/nginx-zen-notes.conf` into the existing HTTPS `server` block, then run:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

Verify reads and writes through the public origin:

```bash
curl -sS https://ch.zernanvash.dev/api/zen-notes
```

## Back up or reset edits

```bash
sudo cp /var/lib/h4g-zen-notes/notes.json /var/lib/h4g-zen-notes/notes.backup.json
sudo systemctl stop zen-notes.service
sudo rm /var/lib/h4g-zen-notes/notes.json
sudo systemctl start zen-notes.service
```

Removing `notes.json` resets the page to the Git-generated source notes. This endpoint intentionally has no authentication; monitor its journal and back up the state file if the public edits matter.
