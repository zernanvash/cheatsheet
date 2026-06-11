# Machine Attack Blueprint Index

Choose one of these blueprints after the first full-port scan and basic service enumeration. The goal is to classify the challenge by evidence, then follow a repeatable path with fallback options.

Sources used for this first blueprint pass:

- `_source_tryhackme_cajac`
- `_source_0xb0b_tryhackme`
- `_source_hackmyvm_writeups`
- `_source_picoctf_cajac`
- `_source_sec_fortress`
- `_source_temperance`
- [Soupedecode 01](https://0xb0b.gitbook.io/writeups/tryhackme/2025/soupedecode-01.md)
- [Cajac TryHackMe Writeups](https://github.com/Cajac/TryHackMe-Writeups)
- [0xb0b TryHackMe GitBook](https://0xb0b.gitbook.io/writeups/tryhackme/)

## Fast Picker

- AD ports `53/88/389/445/464/3268/5985` -> [AD Kerberoasting Chain](AD%20Kerberoasting%20Chain.md), [AD AS-REP Roasting Chain](AD%20AS-REP%20Roasting%20Chain.md), [AD DCSync And Pass-The-Hash Chain](AD%20DCSync%20And%20Pass-The-Hash%20Chain.md)
- AD CS web enrollment or certificate services -> [ADCS ESC1 Chain](ADCS%20ESC1%20Chain.md)
- NetNTLM capture opportunity -> [NTLM Theft And Responder](NTLM%20Theft%20And%20Responder.md)
- SMB readable as guest/null -> [SMB Shares To Credentials](SMB%20Shares%20To%20Credentials.md)
- valid Windows creds or hashes -> [WinRM And RDP Access](WinRM%20And%20RDP%20Access.md)
- WebDAV methods -> [WebDAV PUT And MOVE To Shell](WebDAV%20PUT%20And%20MOVE%20To%20Shell.md)
- SSRF, PDF generator, webhook, internal fetch -> [SSRF And Internal Admin Panels](SSRF%20And%20Internal%20Admin%20Panels.md)
- web app with upload -> [Web Upload To Shell](Web%20Upload%20To%20Shell.md)
- web file parameter -> [LFI And Directory Traversal](LFI%20And%20Directory%20Traversal.md)
- XML/SOAP/document parser -> [XXE To File Read](XXE%20To%20File%20Read.md)
- template expression reflection -> [SSTI To RCE](SSTI%20To%20RCE.md)
- Node.js merge/object bug -> [Prototype Pollution And Node RCE](Prototype%20Pollution%20And%20Node%20RCE.md)
- file/source/backup leak -> [File Disclosure And Source Review](File%20Disclosure%20And%20Source%20Review.md)
- readable log plus LFI -> [Log Poisoning To RCE](Log%20Poisoning%20To%20RCE.md)
- web command wrapper -> [Command Injection To Shell](Command%20Injection%20To%20Shell.md)
- database-backed web app -> [SQL Injection To Credentials](SQL%20Injection%20To%20Credentials.md)
- WordPress/Tomcat/Jenkins/CMS signal -> [CMS And Framework Exploitation](CMS%20And%20Framework%20Exploitation.md)
- Webmin/admin console signal -> [Webmin And Admin Console RCE](Webmin%20And%20Admin%20Console%20RCE.md)
- Nginx Unit control API -> [Nginx Unit API Abuse](Nginx%20Unit%20API%20Abuse.md)
- MSSQL open -> [MSSQL To Command Execution](MSSQL%20To%20Command%20Execution.md)
- CMS/framework/version signal -> [Known CVE Service Exploitation](Known%20CVE%20Service%20Exploitation.md)
- FTP anonymous or leaked creds -> [FTP To Credentials](FTP%20To%20Credentials.md)
- SSH keys or reused passwords -> [SSH Key And Credential Reuse](SSH%20Key%20And%20Credential%20Reuse.md)
- DNS/SMTP user leaks -> [DNS And SMTP Enumeration](DNS%20And%20SMTP%20Enumeration.md)
- NFS exports -> [NFS Export Abuse](NFS%20Export%20Abuse.md)
- SNMP open -> [SNMP Enumeration To Foothold](SNMP%20Enumeration%20To%20Foothold.md)
- Redis/Memcached open -> [Data Store Exposure](Data%20Store%20Exposure.md)
- port knock hint -> [Port Knocking](Port%20Knocking.md)
- TFTP/UDP file clue -> [TFTP And UDP File Discovery](TFTP%20And%20UDP%20File%20Discovery.md)
- rsync or backup mirror -> [Rsync And Backup Shares](Rsync%20And%20Backup%20Shares.md)
- restricted shell -> [Restricted Shell Escape](Restricted%20Shell%20Escape.md)
- encrypted archive, KeePass, ZIP, GPG, backup -> [Archive And Password Manager Cracking](Archive%20And%20Password%20Manager%20Cracking.md)
- exposed internal route/API reference -> [Exposed API And Internal Host References](Exposed%20API%20And%20Internal%20Host%20References.md)
- packet capture artifact -> [PCAP And Traffic Artifact To Credentials](PCAP%20And%20Traffic%20Artifact%20To%20Credentials.md)
- Linux shell -> [Linux Privilege Escalation Blueprint](Linux%20Privilege%20Escalation%20Blueprint.md)
- Linux shell in container or Docker group -> [Docker And Container Escape](Docker%20And%20Container%20Escape.md)
- writable PATH/library/environment influence -> [Environment Variable And Library Hijack](Environment%20Variable%20And%20Library%20Hijack.md)
- Windows shell -> [Windows Privilege Escalation Blueprint](Windows%20Privilege%20Escalation%20Blueprint.md)
- internal-only service found -> [Pivoting And Internal Services](Pivoting%20And%20Internal%20Services.md)

## Evidence Groups

- **Credential-first**: FTP, SMB, NFS, source leaks, archives, PCAPs, SMTP users, SNMP users, AD roasting.
- **Web-to-shell**: upload, command injection, SSTI, WebDAV, CMS/admin console CVE, log poisoning, SSRF to internal admin.
- **File-read-to-foothold**: LFI/traversal, XXE, backup/source disclosure, exposed API routes, Nginx Unit config.
- **Windows/AD**: Kerberoasting, AS-REP, NTLM capture, pass-the-hash, MSSQL, ADCS ESC1, WinRM/RDP.
- **Linux privesc**: sudo, SUID, capabilities, cron, environment/library hijack, Docker/container, kernel only after easier checks.
- **Artifact support**: pcap analysis, archive cracking, crypto/stego hints, reverse engineering, buffer overflow.

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

## If Stuck

- Re-run content discovery with extensions and discovered words.
- Build a username list from pages, SMB files, SMTP, SNMP, certificates, and `/etc/passwd`.
- Search downloaded files for `password`, `user`, `key`, `token`, `backup`, `db`, and `connection`.
- Try recovered credentials across SSH, SMB, WinRM, RDP, FTP, CMS admin, databases, and internal panels.
- Check UDP and uncommon services if TCP leads are exhausted.
- Revisit every source leak after learning the framework, hostname, or username format.
