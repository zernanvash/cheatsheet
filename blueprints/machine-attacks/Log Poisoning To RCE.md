# Log Poisoning To RCE

Use when LFI reads web, SSH, FTP, or mail logs and a service writes user-controlled text into that log.

## Signals

- LFI can read `/var/log/apache2/access.log`, `/var/log/nginx/access.log`, auth logs, FTP logs, or mail logs.
- User-Agent, URL path, username, or mail content appears in the log.
- PHP or similar interpreter executes included log content.

## Main Path

```bash
curl -A 'probe-log-poison' http://target/
curl 'http://target/index.php?page=/var/log/apache2/access.log'
```

Confirm that your marker appears before trying code execution. Keep proof minimal and lab-scoped.

## Options To Try

- Poison User-Agent, request path, referer, SSH username, FTP username, or mail body.
- Try Apache, Nginx, PHP-FPM, auth, vsFTPd, and mail logs.
- If PHP tags are filtered, try different log sources or wrappers.
- If log read works but execution does not, use it only for data disclosure.

## Study Examples

- HackMyVM `Medusa`: LFI and vsFTPd log poisoning pattern appears in the machine chain.
- Common boot2root rooms use this after normal traversal proves file read but no direct credentials.
