# NFS Export Abuse

Use when NFS/RPC services expose mounts.

## Signals

- Ports `111`, `2049`, or `mountd` high ports.
- `showmount -e target` returns exports.
- Export options include weak access control or `no_root_squash`.

## Main Path

```bash
showmount -e target
mkdir -p nfs
sudo mount -t nfs -o vers=3,nolock target:/export nfs
find nfs -maxdepth 3 -type f -ls
```

Look for:

- SSH keys
- backups
- web roots
- writable scripts
- UID/GID ownership clues

## Options To Try

- If `no_root_squash`, create a root-owned SUID helper in the export and execute from target context where appropriate.
- If UID mismatch blocks reads, create a local user with matching UID or use `sudo` carefully.
- If export is web root, upload a web shell or modify writable app files in lab scope.
- If only read access, search for credentials and keys.
- Try NFS versions `3` and `4` if mounting fails.

## Study Examples

- Common Linux boot2root pattern: NFS read/write gives SSH key, web shell, or local privilege escalation.
