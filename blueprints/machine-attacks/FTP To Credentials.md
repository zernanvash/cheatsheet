# FTP To Credentials

Use when FTP is open or files are retrievable from anonymous or reused credentials.

## Signals

- Port `21` open.
- Anonymous login works.
- FTP exposes web root, backups, logs, or user files.
- Credentials from FTP work elsewhere.

## Main Path

```bash
ftp target
wget -m ftp://anonymous:anonymous@target/
hydra -l user -P /usr/share/wordlists/rockyou.txt ftp://target
```

Search downloaded files:

```bash
grep -RniE 'pass|password|user|secret|token|key' .
find . -iname '*.zip' -o -iname '*.bak' -o -iname '*.config' -o -iname 'id_rsa'
```

## Options To Try

- If upload is allowed and FTP maps to web root, test web execution path.
- If logs are writable/readable, check log poisoning paths with LFI.
- If credentials work for FTP, test SSH, SMB, WinRM, web admin, and database services.
- If archives are password-protected, use `zip2john`, `rar2john`, or `7z2john`.
- If only filenames are visible, infer app stack and brute-force web paths.

## Study Examples

- Cajac TryHackMe writeups include FTP enumeration, anonymous download, and credential-reuse patterns across multiple easy rooms.
