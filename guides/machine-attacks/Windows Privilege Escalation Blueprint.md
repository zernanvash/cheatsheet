# Windows Privilege Escalation Blueprint

Use after landing a Windows shell, WinRM, RDP, or web shell.

## Signals

- Commands are `cmd.exe` or PowerShell.
- Paths include `C:\Users`, IIS, services, scheduled tasks.
- `whoami /priv` and service permissions matter.

## Main Path

```cmd
whoami
whoami /priv
whoami /groups
hostname
systeminfo
ipconfig /all
net user
net localgroup administrators
cmdkey /list
```

PowerShell:

```powershell
Get-LocalUser
Get-LocalGroupMember Administrators
Get-Service * | Select DisplayName,Status,ServiceName,Can*
Get-CimInstance -ClassName win32_service | Select Name,State,PathName
```

## Options To Try

- `SeImpersonatePrivilege` -> Potato-family lab path after OS/build check.
- Service config writable -> change path or binary in scope.
- Unquoted service path -> only if writable parent component exists.
- DLL hijacking -> missing/unsafe DLL load with writable path.
- `AlwaysInstallElevated` -> MSI path if both registry values are set.
- Saved creds -> `cmdkey /list`, `runas /savecred`, credential XML.
- Readable SAM/SYSTEM/SECURITY -> offline extraction.
- Scheduled task writable script -> controlled proof then shell.
- Local admin but medium integrity -> UAC bypass study path if allowed.

## Study Examples

- Hexdump Windows privesc course notes integrated in local Windows sheets.
- Cajac Windows exploitation basics and AD challenge writeups.
