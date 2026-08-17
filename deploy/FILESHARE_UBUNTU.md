# Deploy the public file share

The service is deliberately unauthenticated. Files are stored outside the Git checkout at `/var/lib/h4g-fileshare/files`; `git pull` will not erase them. Downloads use `application/octet-stream` plus `Content-Disposition: attachment`, so uploaded HTML or scripts are not previewed by this service.

## Install the service

```bash
sudo useradd --system --home /var/lib/h4g-fileshare --create-home --shell /usr/sbin/nologin h4g-fileshare
sudo install -m 644 deploy/fileshare.service /etc/systemd/system/fileshare.service
sudo systemctl daemon-reload
sudo systemctl enable --now fileshare.service
curl http://127.0.0.1:8789/health
```

## Set upload and storage limits

Edit `/etc/systemd/system/fileshare.service`:

```ini
Environment=FILESHARE_MAX_FILE_BYTES=104857600
Environment=FILESHARE_MAX_TOTAL_BYTES=10737418240
```

The defaults are 100 MiB per file and 10 GiB total. After changing them:

```bash
sudo systemctl daemon-reload
sudo systemctl restart fileshare.service
```

Also set `client_max_body_size` in `deploy/nginx-fileshare.conf` to the same or a larger per-file value. Nginx values such as `100m` use MiB-style units.

## Configure Nginx

Copy all locations from `deploy/nginx-fileshare.conf` into the existing HTTPS `server` block, then run:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

Open `https://ch.zernanvash.dev/fileshare/` and upload a small test file.

## Back up storage

Stop the service for a consistent index-and-files backup:

```bash
sudo systemctl stop fileshare.service
sudo tar -C /var/lib -czf /var/backups/h4g-fileshare.tar.gz h4g-fileshare
sudo systemctl start fileshare.service
```

Because uploads are public, monitor free disk space and the service journal. The total quota prevents this service from intentionally consuming more than its configured allocation, but filesystem space should still be monitored.
