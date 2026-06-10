# Service Enumeration Alternatives

Integrated from Sec-Fortress QuickEnum and writeup patterns. Use in authorized labs and assessments.

## Infrastructure

- Certificate transparency: `curl -s 'https://crt.sh/?q=domain.com&output=json' | jq .`
- Shodan per-IP sweep: `for i in $(cat ip-addresses.txt); do shodan host $i; done`
- Add discovered hostnames to `/etc/hosts` when virtual hosts or AD DNS names appear.

## FTP

- `ftp ip`
- `nc -nv ip 21`
- `telnet ip 21`
- `openssl s_client -connect ip:21 -starttls ftp`
- `wget -m --no-passive ftp://anonymous:anonymous@ip/`

Alternative checks:

- anonymous read/write
- uploaded files reachable from web root
- FTP logs readable through LFI
- backup archives or `.pcap` files

## SMB / RPC

- `smbclient -N -L //ip`
- `smbclient //ip/share`
- `rpcclient -U "" ip`
- `samrdump.py ip`
- `smbmap -H ip`
- `crackmapexec smb ip --shares -u '' -p ''`
- `enum4linux-ng.py ip -A`

Alternative branches:

- writable share -> test upload and user interaction
- readable `SYSVOL` -> search scripts and credentials
- null session -> enumerate users and descriptions
- NTLM theft via writable share in AD labs

## NFS

- `showmount -e ip`
- `mkdir target-NFS`
- `sudo mount -t nfs -o vers=3,nolock ip:/share ./target-NFS`
- `sudo umount ./target-NFS`

Check:

- `no_root_squash`
- readable SSH keys
- backups
- UID/GID mismatches that let you create a matching local user

## DNS

- `dig ns domain.tld @nameserver`
- `dig any domain.tld @nameserver`
- `dig axfr domain.tld @nameserver`
- `dnsenum --dnsserver nameserver --enum -p 0 -s 0 -o found_subdomains.txt -f subdomains.list domain.tld`

Alternative branches:

- zone transfer -> enumerate hosts
- stale CNAME -> takeover check
- split-horizon DNS -> query internal nameserver directly

## SMTP

- `telnet ip 25`
- `nc -nv ip 25`
- `smtp-user-enum -M VRFY -U users.txt -t ip`
- try `VRFY user` and `EXPN list` manually

Use results for:

- username list
- password spraying in labs
- phishing simulation only when explicitly scoped

## IMAP / POP3

- `openssl s_client -connect ip:imaps`
- `openssl s_client -connect ip:pop3s`
- `curl -k 'imaps://ip' --user user:password`

Check mail for:

- credentials
- reset links
- internal hostnames
- attachments

## SNMP

- `snmpwalk -v2c -c public ip`
- `onesixtyone -c community-strings.list ip`
- `braa public@ip:.1.*`

Look for:

- running processes
- network interfaces
- usernames
- installed software
- contact/location strings

## Databases

MySQL:

- `mysql -u user -p -h ip`

MSSQL:

- `impacket-mssqlclient user:pass@ip -windows-auth`
- `mssqlclient.py user@ip -windows-auth`

Oracle TNS:

- `./odat.py all -s ip`
- `sqlplus user/pass@ip/db`
- `./odat.py utlfile -s ip -d db -U user -P pass --sysdba --putFile C:\\path file.txt ./file.txt`

Redis/Memcached:

- `redis-cli -h ip`
- `nc ip 11211`

## IPMI

- Metasploit `auxiliary/scanner/ipmi/ipmi_version`
- Metasploit `auxiliary/scanner/ipmi/ipmi_dumphashes`

If a hash is recovered, crack offline and test only in scope.

## Remote Management

Linux:

- `ssh-audit.py ip`
- `ssh user@ip`
- `ssh -i private.key user@ip`
- `ssh user@ip -o PreferredAuthentications=password`

Windows:

- `rdp-sec-check.pl ip`
- `xfreerdp /u:user /p:'password' /v:ip /cert:ignore /dynamic-resolution`
- `evil-winrm -i ip -u user -p password`
- `evil-winrm -i ip -u user -H NT_HASH`
- `impacket-wmiexec user:'password'@ip 'whoami'`

