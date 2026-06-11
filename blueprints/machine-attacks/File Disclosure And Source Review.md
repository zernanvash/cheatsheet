# File Disclosure And Source Review

Use when discovery finds backups, source archives, `.git`, config files, debug output, or readable deployment artifacts.

## Signals

- Files: `.env`, `web.config`, `config.php`, `settings.py`, `.bak`, `.old`, `.zip`, `.tar`, `.sql`, `.git`.
- Directory listing or backup folders.
- Error pages reveal framework paths or stack traces.
- Source code is intentionally downloadable.

## Main Path

```bash
ffuf -u http://target/FUZZ -w /usr/share/seclists/Discovery/Web-Content/common.txt -e .php,.txt,.bak,.old,.zip,.tar,.sql
grep -RniE 'pass|password|pwd|secret|token|key|db_|connection' .
```

Review source for database credentials, hardcoded users, upload paths, command wrappers, unsafe deserialization, and internal hostnames.

## Options To Try

- If `.git` is exposed, recover history and search old commits.
- If a database dump is found, crack hashes and test credential reuse.
- If framework source is available, identify route handlers and dangerous sinks.
- If config gives DB access, enumerate users, hashes, and app secrets.
- If source shows file read, upload, command execution, or SSRF, move to that blueprint.

## Study Examples

- HackMyVM `Observer`: file read exposes SSH keys and history.
- Sec-Fortress `Lazy Admin`: file disclosure leads to application access and RCE.
- TryHackMe `Smol`: WordPress plugin LFI enables config/source review.
