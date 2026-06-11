# Nginx Unit API Abuse

Use when Nginx Unit is exposed locally or remotely and the control API can change application configuration.

## Signals

- Nmap or headers identify Nginx Unit.
- Port exposes JSON config endpoints.
- Local shell finds Unit socket or control port.
- Web behavior suggests dynamic app routing through Unit.

## Main Path

```bash
curl -s http://target:PORT/config/
curl -s http://127.0.0.1:PORT/config/
```

Inspect listeners, applications, working directories, users, and script paths. In labs, controlled config changes may allow file placement or command execution depending on application type.

## Options To Try

- Check whether the API is only bound to localhost, then use SSRF or pivoting if in scope.
- Look for writable app roots or upload paths referenced by Unit config.
- Preserve original config before lab changes.
- If direct abuse is blocked, use config disclosure for users, paths, and source review.

## Study Examples

- HackMyVM `Icecream`: SMB and Nginx Unit API appear as part of the service chain.
- Use with [SSRF And Internal Admin Panels](SSRF%20And%20Internal%20Admin%20Panels.md) when the API is internal-only.
