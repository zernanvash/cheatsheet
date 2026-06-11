# Linux Privilege Escalation Blueprint

Use after landing a Linux shell.

## Signals

- Shell commands are Unix-like.
- Paths include `/home`, `/var/www`, `/etc`.
- Kernel, sudo, SUID, cron, capabilities, containers, or app configs become relevant.

## Main Path

```bash
id
whoami
hostname
uname -a
sudo -l
ps auxww
ss -tulpn
find / -perm -4000 -type f -ls 2>/dev/null
getcap -r / 2>/dev/null
cat /etc/crontab
```

Credential search:

```bash
grep -RniE 'pass|password|pwd|secret|token|key' /var/www /opt /home 2>/dev/null
find / -name id_rsa -o -name authorized_keys 2>/dev/null
```

## Options To Try

- `sudo -l` -> GTFOBins or writable config/plugin path.
- SUID binary -> GTFOBins; if custom, inspect with `strings`, `ltrace`, `strace`, `gdb`.
- Writable cron/script -> controlled proof, then shell.
- Capabilities -> `cap_setuid`, `cap_dac_read_search`, `cap_dac_override`.
- App config creds -> try `su`, SSH, DB, web admin.
- Docker socket/group -> inspect host mount paths in lab scope.
- Old kernel -> only after easier misconfigs fail.

## Study Examples

- OSCP Linux module: PATH hijacking, SUID, sudo, wildcard, cron, capabilities, local services, kernel.
- Cajac Linux privesc walkthroughs and common Linux room patterns.
