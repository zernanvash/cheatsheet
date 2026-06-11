# LFI And Directory Traversal

Use when parameters look file-like or route names suggest templates, pages, downloads, or document reads.

## Signals

- Parameters: `file`, `page`, `path`, `doc`, `download`, `template`, `view`.
- Errors reveal local paths.
- URLs include filenames or language/template selectors.

## Main Path

```text
../../../../etc/passwd
..%2f..%2f..%2f..%2fetc%2fpasswd
/var/www/html/index.php
/proc/self/environ
/var/log/apache2/access.log
/var/log/nginx/access.log
```

Use reads to find:

- users and home directories
- app source and configs
- database credentials
- SSH keys
- logs for poisoning only when confirmed and in scope

## Options To Try

- Encoding: URL encoding, double encoding, null-byte only on old stacks, path normalization tricks.
- Absolute paths after relative paths fail.
- Windows paths if target is IIS: `C:\Windows\win.ini`, `web.config`.
- Read source files instead of jumping to shell.
- If logs are readable, test controlled log poisoning with harmless command proof before shell.

## Study Examples

- OSCP/web module directory traversal and file inclusion topics map here.
- TryHackMe web writeups often use traversal to collect credentials before SSH or admin login.
