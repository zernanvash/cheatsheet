# SSRF And Internal Admin Panels

Use when a web app fetches URLs, renders PDFs, imports remote files, checks webhooks, or proxies requests.

## Signals

- Features: URL preview, PDF generation, image fetch, webhook test, import from URL.
- Errors reveal `localhost`, cloud metadata, internal IPs, or blocked schemes.
- Public app can reach a service you cannot scan directly.

## Main Path

```bash
curl -i 'http://target/fetch?url=http://127.0.0.1:80/'
curl -i 'http://target/fetch?url=http://127.0.0.1:8080/'
```

Confirm server-side fetch with a controlled listener or harmless internal read. Then map localhost ports and internal hostnames within scope.

## Options To Try

- Try `127.0.0.1`, `localhost`, IPv6 localhost, decimal/hex IP encoding, and discovered hostnames.
- Test allowed schemes: `http`, `https`, `file`, `gopher` only when the lab expects it.
- Look for admin panels, Redis, Nginx Unit, cloud metadata, and local-only debug routes.
- If SSRF returns blind, use callback timing or DNS logs in lab infrastructure.

## Study Examples

- Sec-Fortress `MD2PDF`: PDF generation/SSRF pattern.
- Use with [Nginx Unit API Abuse](Nginx%20Unit%20API%20Abuse.md) or [Exposed API And Internal Host References](Exposed%20API%20And%20Internal%20Host%20References.md).
