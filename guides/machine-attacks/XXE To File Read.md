# XXE To File Read

Use when XML parsing is reachable through SOAP, SAML, document upload, SVG, DOCX, or API requests.

## Signals

- XML body accepted by the app.
- SOAP endpoint, SAML login, SVG upload, or office document parser.
- Error messages mention XML parser, entity, DTD, or external resource.

## Main Path

```xml
<?xml version="1.0"?>
<!DOCTYPE root [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<root>&xxe;</root>
```

Prove file read with a safe local file, then target app configs, web roots, users, and keys.

## Options To Try

- Use blind XXE with external DTD callback when output is not reflected.
- Test Windows file paths on IIS or Windows services.
- Try SVG or DOCX containers when raw XML is not accepted.
- If file read gives credentials, pivot to SSH, SMB, WinRM, DB, or admin panels.

## Study Examples

- Sec-Fortress `Muddy`: XXE appears before WebDAV/Cron progression.
- HackTheBox/TryHackMe `Bounty Hunter`: XXE leads into a Python privilege escalation path.
