# Footprinting Cheat Sheet

Fast command selector for turning a domain, IP, or open service into evidence and next actions. Expanded from the local `Footprinting - cheatsheet.pdf` and linked into the existing local recon sheets.

## When To Use

Use this after initial scope setup and before exploitation. The goal is to answer:

- What hosts, names, and services exist?
- Which services allow anonymous, guest, default, or weak authentication?
- Which files, users, hostnames, hashes, or credentials can be collected safely?
- Which blueprint should be opened next?

## Pick By Signal

| Signal | Run first | Then open |
|---|---|---|
| Domain name only | Certificate transparency, DNS, whois, search operators | [Passive Recon](Passive%20Recon.md), [Dig Cheat Sheet](Dig%20Cheat%20Sheet.md) |
| IP list or public IP range | Shodan sweep, nmap service scan | [Nmap Cheat Sheet](Nmap%20Cheat%20Sheet.md), [Service Enumeration Alternatives](Service%20Enumeration%20Alternatives.md) |
| FTP `21` | anonymous login, mirror files, banner check | [FTP Cheat Sheet](FTP%20Cheat%20Sheet.md) |
| SMB `139/445` | null session, share listing, RPC users | [SMBClient Cheat Sheet](SMBClient%20Cheat%20Sheet.md), [Active Directory Attack Path Cheat Sheet](Active%20Directory%20Attack%20Path%20Cheat%20Sheet.md) |
| NFS `111/2049` | exported shares, mount, inspect files | [Service Enumeration Alternatives](Service%20Enumeration%20Alternatives.md#nfs) |
| DNS `53` | NS/ANY/AXFR, subdomain brute force | [Dig Cheat Sheet](Dig%20Cheat%20Sheet.md), [DNS And SMTP Enumeration](../blueprints/machine-attacks/DNS%20And%20SMTP%20Enumeration.md) |
| SMTP or mail ports | banner, VRFY/EXPN/RCPT, IMAP/POP login | [SMTP](SMTP.md), [DNS And SMTP Enumeration](../blueprints/machine-attacks/DNS%20And%20SMTP%20Enumeration.md) |
| SNMP `161` | community string checks, OID walk | [Service Enumeration Alternatives](Service%20Enumeration%20Alternatives.md#snmp) |
| MySQL, MSSQL, Oracle | login test, version, database-specific enum | [Service Enumeration Alternatives](Service%20Enumeration%20Alternatives.md#databases) |
| SSH, RDP, WinRM | audit, login with recovered creds, remote exec | [Service Enumeration Alternatives](Service%20Enumeration%20Alternatives.md#remote-management) |
| IPMI `623` | version and hash dump modules | [Service Enumeration Alternatives](Service%20Enumeration%20Alternatives.md#ipmi) |

## Infrastructure Enumeration

Use this when you have a domain, organization name, or a list of public IPs.

```bash
curl -s 'https://crt.sh/?q=example.com&output=json' | jq .
for i in $(cat ip-addresses.txt); do shodan host "$i"; done
whois example.com
dig example.com NS +short
dig example.com MX +short
dig example.com TXT +short
```

What to keep:

- subdomains and alternate hostnames
- mail servers and naming patterns
- technologies from banners, titles, certs, and TXT records
- usernames, emails, and naming conventions
- cloud provider or CDN hints

## Host-Based Footprinting

Run these only against scoped targets.

### FTP

```bash
ftp target
nc -nv target 21
telnet target 21
openssl s_client -connect target:21 -starttls ftp
wget -m --no-passive ftp://anonymous:anonymous@target/
```

Use findings for backups, source code, notes, upload paths, and credentials to test on SSH, SMB, web login, and databases.

### SMB And RPC

```bash
smbclient -N -L //target
smbclient //target/share
rpcclient -U "" target
samrdump.py target
smbmap -H target
crackmapexec smb target --shares -u '' -p ''
enum4linux-ng.py target -A
```

Use findings for readable shares, writable shares, domain names, users, RIDs, scripts, `SYSVOL`, Group Policy Preferences, and credential reuse.

### NFS

```bash
showmount -e target
mkdir -p target-NFS
sudo mount -t nfs -o vers=3,nolock target:/share ./target-NFS
sudo umount ./target-NFS
```

Check for SSH keys, backups, UID/GID ownership issues, and `no_root_squash`.

### DNS

```bash
dig ns domain.tld @nameserver
dig any domain.tld @nameserver
dig axfr domain.tld @nameserver
dnsenum --dnsserver nameserver --enum -p 0 -s 0 -o found_subdomains.txt -f subdomains.list domain.tld
```

If AXFR works, add discovered names to `/etc/hosts`, rescan vhosts, and check for AD naming patterns.

### SMTP, IMAP, And POP3

```bash
nc -nv target 25
telnet target 25
smtp-user-enum -M VRFY -U users.txt -t target
smtp-user-enum -M RCPT -U users.txt -t target
openssl s_client -connect target:993
openssl s_client -connect target:995
curl -k 'imaps://target' --user user:password
```

Use findings for valid usernames, password attack inputs, reset links, internal hostnames, and attachments.

### SNMP

```bash
snmpwalk -v2c -c public target
onesixtyone -c community-strings.list target
braa public@target:.1.*
```

Look for users, running processes, installed software, interfaces, routes, contact strings, and leaked service names.

### Databases

```bash
mysql -u user -p -h target
mssqlclient.py user@target -windows-auth
./odat.py all -s target
sqlplus user/pass@target/db
./odat.py utlfile -s target -d db -U user -P pass --sysdba --putFile C:\\path file.txt ./file.txt
```

Use database access to enumerate users, credentials, file read/write primitives, command execution features, and service account context.

### IPMI

```text
use auxiliary/scanner/ipmi/ipmi_version
use auxiliary/scanner/ipmi/ipmi_dumphashes
```

If hashes are dumped, crack offline and test only within scope.

### Remote Management

```bash
ssh-audit.py target
ssh user@target
ssh -i private.key user@target
ssh user@target -o PreferredAuthentications=password
rdp-sec-check.pl target
xfreerdp /u:user /p:'password' /v:target /cert:ignore /dynamic-resolution
evil-winrm -i target -u user -p password
wmiexec.py user:'password'@target 'whoami'
```

Use remote management after credentials, keys, hashes, or password reuse are discovered.

## Output Discipline

Save raw output and extracted notes separately:

```bash
mkdir -p scans loot notes
nmap -sC -sV -oA scans/initial target
tee notes/footprinting-findings.md
```

Track each finding as:

```text
Service:
Command:
Finding:
Why it matters:
Next file to open:
Next command to try:
```

## Related

- [Passive Recon](Passive%20Recon.md)
- [Service Enumeration Alternatives](Service%20Enumeration%20Alternatives.md)
- [Nmap Cheat Sheet](Nmap%20Cheat%20Sheet.md)
- [Networking](Networking.md)
