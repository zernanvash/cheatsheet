# WebDAV PUT And MOVE To Shell

Use when HTTP methods expose WebDAV write or move behavior.

## Signals

- `OPTIONS` shows `PUT`, `MOVE`, `COPY`, `PROPFIND`, or WebDAV headers.
- Nmap scripts identify WebDAV.
- Upload is not visible in the app, but HTTP methods allow file placement.

## Main Path

```bash
curl -i -X OPTIONS http://target/
curl -i -X PUT --data-binary @proof.txt http://target/proof.txt
curl -i http://target/proof.txt
```

If executable extensions are blocked, try placing a harmless text proof first and then test stack-appropriate extensions only in lab scope.

## Options To Try

- Use `MOVE` to rename an allowed upload extension to executable extension.
- Try authenticated WebDAV with recovered credentials.
- Check writable subdirectories, not only web root.
- If execution fails, use WebDAV for file disclosure, staging, or NTLM capture in Windows labs.

## Study Examples

- Sec-Fortress `Muddy`: XXE/WebDAV PUT/Cron chain.
- Common IIS and Apache WebDAV labs use method enumeration as the foothold pivot.
