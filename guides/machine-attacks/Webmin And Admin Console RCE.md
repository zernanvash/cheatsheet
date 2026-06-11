# Webmin And Admin Console RCE

Use when a known admin console is exposed: Webmin, Jenkins, Tomcat Manager, cockpit, phpMyAdmin, CUPS, or similar.

## Signals

- Service title, favicon, headers, or paths identify an admin product.
- Version is visible and maps to a known CVE.
- Recovered credentials work on an admin panel.
- Console has script, plugin, job, package, file manager, or terminal features.

## Main Path

```bash
whatweb http://target:PORT/
searchsploit product version
nmap -sC -sV -p PORT target
```

Confirm version and authentication state. Prefer built-in admin features or verified exploit modules only when the lab clearly supports them.

## Options To Try

- Try default credentials only where the lab scope permits.
- Search for backup configs that contain admin passwords.
- For Jenkins/Tomcat, check deploy/script console paths.
- For Webmin, verify exact version and module before using Metasploit or public PoC.
- If the console is internal-only, combine with SSRF or pivoting.

## Study Examples

- Sec-Fortress `Source`: Webmin/Metasploit-style exploitation.
- Sec-Fortress `Ignite`: Fuel CMS admin/RCE and password-in-config pattern.
