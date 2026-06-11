# Exposed API And Internal Host References

Use when public content references API endpoints, hostnames, internal IPs, GraphQL, Swagger, JavaScript routes, or admin-only services.

## Signals

- JavaScript contains `/api/`, tokens, internal hostnames, or debug routes.
- Swagger/OpenAPI, GraphQL playground, or API docs are exposed.
- HTML comments, source maps, or config files reveal internal services.
- Error responses disclose backend URLs.

## Main Path

```bash
curl -i http://target/
curl -s http://target/app.js | grep -Ei 'api|token|admin|internal|debug'
ffuf -u http://target/FUZZ -w /usr/share/seclists/Discovery/Web-Content/api/api-endpoints.txt
```

Map endpoints, authentication requirements, methods, and object IDs before trying exploit branches.

## Options To Try

- Download source maps and reconstruct client-side routes.
- Test IDOR only with lab-owned objects.
- Try method changes: `GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `OPTIONS`.
- Add discovered hostnames to `/etc/hosts` and repeat vhost discovery.
- If internal URLs are only server-fetchable, switch to [SSRF And Internal Admin Panels](SSRF%20And%20Internal%20Admin%20Panels.md).

## Study Examples

- HMV and Sec-Fortress web-first machines often expose hidden routes through comments, JavaScript, or API errors.
- picoCTF web challenges are useful support practice for source review and route extraction.
