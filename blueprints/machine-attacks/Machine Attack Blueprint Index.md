# Machine Attack Blueprint Index

Use this after your first full TCP scan and basic service enumeration. Match what you have seen, open the smallest template that fits, and come back here when new evidence appears.

## Baseline Before Choosing

```bash
nmap -p- --min-rate 5000 -oN ports.txt target
nmap -sC -sV -O -p PORTS -oN nmap.txt target
nmap -sU --top-ports 100 -oN udp.txt target
```

Classify first:

- AD/domain: Kerberos, LDAP, DNS, SMB, Global Catalog, WinRM, domain names.
- Linux service box: SSH, Apache/Nginx, Samba on Linux, NFS, SNMP, Unix paths, cron/SUID hints.
- Windows standalone: native SMB, WinRM, RDP, IIS, MSSQL, Windows paths without domain signals.
- Web-first: HTTP discovery gives source, upload, file read, injection, admin panel, or CVE.
- Artifact-first: pcap, archive, KeePass, hashes, stego/crypto, binary, or source bundle.

## Windows And AD

| Signal | Blueprint |
|---|---|
| Kerberos/LDAP/DNS/SMB domain ports | [AD Kerberoasting Chain](AD%20Kerberoasting%20Chain.md), [AD AS-REP Roasting Chain](AD%20AS-REP%20Roasting%20Chain.md) |
| Domain admin hash, replication rights, or high-priv domain creds | [AD DCSync And Pass-The-Hash Chain](AD%20DCSync%20And%20Pass-The-Hash%20Chain.md) |
| AD CS, `certsrv`, certificate templates, enrollment rights | [ADCS ESC1 Chain](ADCS%20ESC1%20Chain.md) |
| NetNTLM capture path, writable SMB, LNK/UNC callback | [NTLM Theft And Responder](NTLM%20Theft%20And%20Responder.md) |
| Valid Windows password/hash and remote access ports | [WinRM And RDP Access](WinRM%20And%20RDP%20Access.md) |
| MSSQL port or SQL Server creds | [MSSQL To Command Execution](MSSQL%20To%20Command%20Execution.md) |
| Windows shell landed | [Windows Privilege Escalation Blueprint](Windows%20Privilege%20Escalation%20Blueprint.md) |

## Credential And File First

| Signal | Blueprint |
|---|---|
| Guest/null SMB, readable shares, writable shares | [SMB Shares To Credentials](SMB%20Shares%20To%20Credentials.md) |
| FTP anonymous, FTP creds, upload/download path | [FTP To Credentials](FTP%20To%20Credentials.md) |
| SSH key, cracked password, reused credential | [SSH Key And Credential Reuse](SSH%20Key%20And%20Credential%20Reuse.md) |
| NFS exports, UID/GID mismatch, `no_root_squash` | [NFS Export Abuse](NFS%20Export%20Abuse.md) |
| SNMP open or `public` community | [SNMP Enumeration To Foothold](SNMP%20Enumeration%20To%20Foothold.md) |
| DNS zone transfer or SMTP user leak | [DNS And SMTP Enumeration](DNS%20And%20SMTP%20Enumeration.md) |
| Redis, Memcached, database exposure | [Data Store Exposure](Data%20Store%20Exposure.md) |
| ZIP, 7z, RAR, KeePass, GPG, backup, protected SSH key | [Archive And Password Manager Cracking](Archive%20And%20Password%20Manager%20Cracking.md) |
| PCAP or traffic artifact | [PCAP And Traffic Artifact To Credentials](PCAP%20And%20Traffic%20Artifact%20To%20Credentials.md) |

## Web To Shell And File Read

| Signal | Blueprint |
|---|---|
| Source leak, `.env`, `.git`, backup, config, debug output | [File Disclosure And Source Review](File%20Disclosure%20And%20Source%20Review.md) |
| Upload form, media manager, plugin upload | [Web Upload To Shell](Web%20Upload%20To%20Shell.md) |
| `file`, `page`, `path`, download, template, or traversal behavior | [LFI And Directory Traversal](LFI%20And%20Directory%20Traversal.md) |
| Readable log plus LFI | [Log Poisoning To RCE](Log%20Poisoning%20To%20RCE.md) |
| SQL-backed app, login bypass, database errors | [SQL Injection To Credentials](SQL%20Injection%20To%20Credentials.md) |
| Ping/DNS/PDF/archive/image/admin command wrapper | [Command Injection To Shell](Command%20Injection%20To%20Shell.md) |
| Template syntax reflection or template error | [SSTI To RCE](SSTI%20To%20RCE.md) |
| XML, SOAP, SAML, SVG, DOCX, parser errors | [XXE To File Read](XXE%20To%20File%20Read.md) |
| URL fetcher, PDF generator, webhook, internal-only app | [SSRF And Internal Admin Panels](SSRF%20And%20Internal%20Admin%20Panels.md) |
| Node.js merge/object behavior | [Prototype Pollution And Node RCE](Prototype%20Pollution%20And%20Node%20RCE.md) |
| WebDAV methods: `PUT`, `MOVE`, `PROPFIND` | [WebDAV PUT And MOVE To Shell](WebDAV%20PUT%20And%20MOVE%20To%20Shell.md) |
| WordPress, Tomcat, Jenkins, CMS/admin panel | [CMS And Framework Exploitation](CMS%20And%20Framework%20Exploitation.md), [Webmin And Admin Console RCE](Webmin%20And%20Admin%20Console%20RCE.md) |
| Versioned vulnerable service or framework | [Known CVE Service Exploitation](Known%20CVE%20Service%20Exploitation.md) |
| Nginx Unit control API | [Nginx Unit API Abuse](Nginx%20Unit%20API%20Abuse.md) |
| Exposed API routes, Swagger, GraphQL, internal host references | [Exposed API And Internal Host References](Exposed%20API%20And%20Internal%20Host%20References.md) |

## Linux And Pivoting

| Signal | Blueprint |
|---|---|
| Linux shell landed | [Linux Privilege Escalation Blueprint](Linux%20Privilege%20Escalation%20Blueprint.md) |
| Docker group, socket, container marker | [Docker And Container Escape](Docker%20And%20Container%20Escape.md) |
| PATH/library/environment influence | [Environment Variable And Library Hijack](Environment%20Variable%20And%20Library%20Hijack.md) |
| Restricted shell or menu shell | [Restricted Shell Escape](Restricted%20Shell%20Escape.md) |
| Port knocking hint | [Port Knocking](Port%20Knocking.md) |
| TFTP or UDP file clue | [TFTP And UDP File Discovery](TFTP%20And%20UDP%20File%20Discovery.md) |
| Rsync or backup mirror | [Rsync And Backup Shares](Rsync%20And%20Backup%20Shares.md) |
| Internal-only service found after foothold | [Pivoting And Internal Services](Pivoting%20And%20Internal%20Services.md) |

## If Stuck

- Re-run content discovery with extensions and words found on the target.
- Build a username list from web pages, SMB files, SMTP, SNMP, certificates, and `/etc/passwd`.
- Search downloaded files for `password`, `user`, `key`, `token`, `backup`, `db`, `connection`, and hostnames.
- Try recovered credentials across SSH, SMB, WinRM, RDP, FTP, CMS admin, databases, and internal panels.
- Check UDP and uncommon services if TCP leads are exhausted.
- Revisit source leaks after learning the framework, hostname, username format, or internal path.

## Source Coverage

This index is mined from local TryHackMe, HackMyVM/HMV, picoCTF, Sec-Fortress, Temperance, OSCP module, and challenge-use-case material. Keep source folders in [Source Inventory](../../references/Source%20Inventory.md); use this page as the working selector.
