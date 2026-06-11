# Rsync And Backup Shares

Use when rsync, backup daemons, or mirror directories expose files without normal web/SMB access.

## Signals

- Port `873` open or banners mention rsync.
- Web/source hints mention backup, mirror, sync, or archive.
- Nmap scripts identify rsync modules.

## Main Path

```bash
rsync target::
rsync -av target::module ./module
grep -RniE 'pass|password|pwd|secret|token|key|ssh|db' ./module
```

Treat downloaded modules like source disclosure: search configs, keys, backups, and history.

## Options To Try

- Check write permissions only in lab scope.
- Preserve timestamps and permissions when downloading.
- Look for hidden files, `.ssh`, `.git`, database dumps, and app configs.
- Reuse recovered credentials against SSH, SMB, web admin, and databases.

## Study Examples

- Backup exposure is common across HMV/TryHackMe-style Linux machines even when rsync itself is not always the service.
- Pair this with [File Disclosure And Source Review](File%20Disclosure%20And%20Source%20Review.md).
