# Machine Attack Blueprint Index

Choose one of these blueprints after the first full-port scan and basic service enumeration. The goal is to classify the challenge by evidence, then follow a repeatable path with fallback options.

Sources used for this first blueprint pass:

- `_source_tryhackme_cajac`
- `_source_0xb0b_tryhackme`
- [Soupedecode 01](https://0xb0b.gitbook.io/writeups/tryhackme/2025/soupedecode-01.md)
- [Cajac TryHackMe Writeups](https://github.com/Cajac/TryHackMe-Writeups)
- [0xb0b TryHackMe GitBook](https://0xb0b.gitbook.io/writeups/tryhackme/)

## Fast Picker

- AD ports `53/88/389/445/464/3268/5985` -> [AD Kerberoasting Chain](AD%20Kerberoasting%20Chain.md), [AD AS-REP Roasting Chain](AD%20AS-REP%20Roasting%20Chain.md), [AD DCSync And Pass-The-Hash Chain](AD%20DCSync%20And%20Pass-The-Hash%20Chain.md)
- SMB readable as guest/null -> [SMB Shares To Credentials](SMB%20Shares%20To%20Credentials.md)
- valid Windows creds or hashes -> [WinRM And RDP Access](WinRM%20And%20RDP%20Access.md)
- web app with upload -> [Web Upload To Shell](Web%20Upload%20To%20Shell.md)
- web file parameter -> [LFI And Directory Traversal](LFI%20And%20Directory%20Traversal.md)
- web command wrapper -> [Command Injection To Shell](Command%20Injection%20To%20Shell.md)
- database-backed web app -> [SQL Injection To Credentials](SQL%20Injection%20To%20Credentials.md)
- WordPress/Tomcat/Jenkins/CMS signal -> [CMS And Framework Exploitation](CMS%20And%20Framework%20Exploitation.md)
- MSSQL open -> [MSSQL To Command Execution](MSSQL%20To%20Command%20Execution.md)
- CMS/framework/version signal -> [Known CVE Service Exploitation](Known%20CVE%20Service%20Exploitation.md)
- FTP anonymous or leaked creds -> [FTP To Credentials](FTP%20To%20Credentials.md)
- SSH keys or reused passwords -> [SSH Key And Credential Reuse](SSH%20Key%20And%20Credential%20Reuse.md)
- DNS/SMTP user leaks -> [DNS And SMTP Enumeration](DNS%20And%20SMTP%20Enumeration.md)
- NFS exports -> [NFS Export Abuse](NFS%20Export%20Abuse.md)
- SNMP open -> [SNMP Enumeration To Foothold](SNMP%20Enumeration%20To%20Foothold.md)
- Redis/Memcached open -> [Data Store Exposure](Data%20Store%20Exposure.md)
- Linux shell -> [Linux Privilege Escalation Blueprint](Linux%20Privilege%20Escalation%20Blueprint.md)
- Windows shell -> [Windows Privilege Escalation Blueprint](Windows%20Privilege%20Escalation%20Blueprint.md)
- internal-only service found -> [Pivoting And Internal Services](Pivoting%20And%20Internal%20Services.md)

## Baseline Before Choosing

```bash
nmap -p- --min-rate 5000 -oN ports.txt target
nmap -sC -sV -O -p PORTS -oN nmap.txt target
nmap -sU --top-ports 100 -oN udp.txt target
```

Classify by evidence:

- **AD challenge**: Kerberos, LDAP, DNS, SMB, Global Catalog, WinRM, domain names.
- **Linux service challenge**: SSH, Apache/Nginx, NFS, SNMP, Unix paths, cron/SUID hints.
- **Windows standalone challenge**: SMB, WinRM, RDP, IIS, MSSQL, Windows paths but no domain.
- **Web-first challenge**: HTTP route/content discovery produces source, upload, file read, injection, or CVE.

## How To Use A Blueprint

1. Match the scan signal.
2. Run the minimum enumeration in the blueprint.
3. Take the first branch that produces credentials, file read, shell, or privilege change.
4. If blocked, work through **Options To Try** before abandoning the blueprint.
5. After any credential or hash, re-run SMB/WinRM/SSH/web admin checks because access usually expands.
