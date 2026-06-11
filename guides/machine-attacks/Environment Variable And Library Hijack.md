# Environment Variable And Library Hijack

Use when a privileged Linux process, SUID binary, cron job, or sudo rule trusts PATH, library paths, or environment-controlled files.

## Signals

- Custom SUID binary calls programs by relative name.
- `sudo -l` preserves environment or runs a script.
- Cron or service executes writable scripts.
- Error messages mention missing libraries or relative paths.

## Main Path

```bash
sudo -l
find / -perm -4000 -type f -ls 2>/dev/null
strings ./custom-suid
strace -f ./custom-suid 2>&1 | head
ltrace ./custom-suid 2>&1 | head
```

Prove influence with harmless output first, then use the minimum lab action needed for privilege change.

## Options To Try

- PATH hijack when the binary calls `cp`, `tar`, `sh`, or another command without absolute path.
- `LD_PRELOAD`/`LD_LIBRARY_PATH` only when sudo or the binary permits it.
- Writable script or config referenced by root cron.
- Wildcard abuse in root-run commands such as tar or chown.
- Check architecture and permissions before compiling helpers.

## Study Examples

- HackMyVM `Hommie`: environment variable manipulation appears in the machine chain.
- Sec-Fortress `Hijack`: LD library path style privilege escalation pattern.
- OSCP Linux module patterns: PATH hijacking, SUID, cron, and wildcard privilege escalation.
