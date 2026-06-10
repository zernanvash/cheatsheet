# FTP Cheat Sheet

Use only in authorized labs and assessments.

## Quick Checks

- `nmap -sC -sV -p21 ip`
- `ftp ip`
- `anonymous` / `anonymous` - try anonymous login
- `wget -m ftp://anonymous:anonymous@ip/` - mirror anonymous FTP
- `hydra -l user -P /usr/share/wordlists/rockyou.txt ftp://ip` - password test in labs

## Inside FTP

- `ls` - list files
- `pwd` - show remote path
- `cd dir` - change remote directory
- `get file` - download file
- `mget *` - download many files
- `put file` - upload file
- `binary` - binary transfer mode
- `passive` - toggle passive mode

## What To Look For

- anonymous read/write access
- backup archives
- scripts and source code
- notes with usernames/passwords
- web-root upload paths
- readable FTP logs for log poisoning through LFI

## Common Follow-Ups

- Crack archives with `zip2john`, `rar2john`, or `7z2john`.
- Test recovered credentials on SSH, SMB, web login, and databases.
- If upload is writable and web-accessible, test with a harmless proof file before attempting code execution.

