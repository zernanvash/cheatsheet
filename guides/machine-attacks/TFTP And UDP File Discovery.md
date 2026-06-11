# TFTP And UDP File Discovery

Use when UDP scans or clues point to TFTP or simple unauthenticated file retrieval.

## Signals

- UDP `69` open or filtered with TFTP hints.
- Files or web clues mention firmware, configs, PXE, backups, or boot images.
- Nmap UDP scan finds TFTP or related services.

## Main Path

```bash
nmap -sU -p 69 --script tftp-enum target
tftp target
tftp> get filename
```

Pull known filenames from clues, web paths, config names, usernames, and common TFTP boot filenames.

## Options To Try

- Try `pxelinux.cfg/default`, `config`, `backup`, `id_rsa`, app configs, and clue-derived names.
- Use UDP scan timing patiently; false negatives are common.
- If write is allowed, only place controlled proof files in lab scope.
- Search downloaded files for credentials and internal hosts.

## Study Examples

- HackMyVM `Hommie`: UDP/TFTP and SSH key discovery appear in the foothold chain.
- TFTP often pairs with [SSH Key And Credential Reuse](SSH%20Key%20And%20Credential%20Reuse.md).
