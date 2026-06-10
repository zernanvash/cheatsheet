# Sec-Fortress Writeups Index

Source: https://sec-fortress.github.io/

Sec-Fortress is a public writeup index covering TryHackMe, HackTheBox, PwnTillDawn, Proving Grounds, Vulnyx, HackMyVM, and CTF notes. The front page tags each writeup with techniques, which makes it useful as a pattern checklist.

## Common Patterns To Fold Into RedTeam Machine

- Web enumeration: directory fuzzing, WordPress scanning, file disclosure, LFI/RFI, XXE, SSTI, SQL injection, upload-to-RCE.
- Credential discovery: config files, leaked SSH keys, password descriptions, pcap analysis, KeePass/KDBX, PGP/ASC material, archive cracking.
- Linux privilege escalation: sudo GTFOBins, cron jobs, capabilities, SUID, path manipulation, Docker/LXD, AppArmor, Nginx/ExifTool/kernel CVEs.
- Windows and AD: pass-the-hash, BloodHound, abusing ACEs, constrained delegation, ADCS ESC1, LAPS, DCSync, SeImpersonatePrivilege, AlwaysInstallElevated.
- Pivoting and internal services: WebDAV, Jenkins, ActiveMQ, ThinVNC, ProFTPd mod_copy, SMB/NTLM theft.
- Service enumeration alternatives: NFS, SMTP, IMAP/POP3, SNMP, IPMI, Oracle TNS, RDP security checks, SSH audit.
- Web app methodology: access-control bypasses, IDOR, authentication flaws, information disclosure, file upload bypasses, SSRF, SSTI, SQLi tamper paths.
- Misc/cloud: Google Cloud Storage bucket checks, AWS Route 53/DNS concepts, Azure runbook credential review, ICMP packet clues, port knocking, TFTP.

## Useful Tags Seen On The Index

- `Pass-The-Hash`
- `BloodHound`
- `Abusing ACEs`
- `Constrained Delegations`
- `ADCS`
- `DCSync`
- `Zone transfer`
- `Capabilities`
- `Cron jobs`
- `Docker Privilege Escalation`
- `SUID Privilege Escalation`
- `Command injection`
- `LFI`
- `RFI`
- `XXE`
- `SSTI`
- `File Upload`
- `Steganography`

## How To Use

When stuck on a machine, search the Sec-Fortress index by technique and compare the attack chain against:

- [RedTeam Machine](../RedTeam%20Machine.md)
- [Linux Attack Path Cheat Sheet](Linux%20Attack%20Path%20Cheat%20Sheet.md)
- [Windows Attack Path Cheat Sheet](Windows%20Attack%20Path%20Cheat%20Sheet.md)
- [Active Directory Attack Path Cheat Sheet](../tools/Active%20Directory%20Attack%20Path%20Cheat%20Sheet.md)
- [Service Enumeration Alternatives](../tools/Service%20Enumeration%20Alternatives.md)
- [Web Attack Alternatives](../tools/Web%20Attack%20Alternatives.md)
- [Cloud and Misc Recon Alternatives](../tools/Cloud%20and%20Misc%20Recon%20Alternatives.md)
