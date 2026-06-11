# Networking And Linux Fundamentals

Use this before machine exploitation. This is the baseline needed to understand scans, services, shells, and Linux privilege escalation.

## Network Basics

- IP address: host identity on a network.
- Port: service endpoint on a host.
- TCP: connection-oriented; most web, SSH, SMB, and database services.
- UDP: connectionless; DNS, SNMP, TFTP, and some discovery protocols.
- DNS: name-to-IP mapping.
- Route: where traffic goes next.

Beginner commands:

```bash
ip addr
ip route
ping -c 1 target
nc -nv target 80
```

## Service Thinking

A port is not the goal. The service behind it is the clue.

- `21`: FTP, files, anonymous access, credentials.
- `22`: SSH, shell access, key reuse.
- `25`: SMTP, users and mail behavior.
- `53`: DNS, zone transfers, hostnames.
- `80/443`: web, apps, source, auth, injection.
- `111/2049`: NFS, exports, UID/GID issues.
- `139/445`: SMB, shares, Windows/AD/Samba.
- `161`: SNMP, users, processes, interfaces.
- `3306/5432`: databases.

## Linux Basics

Important commands:

```bash
whoami
id
pwd
ls -la
cat file
find . -type f
grep -Rni 'password' .
```

Important paths:

- `/etc/passwd`: local users.
- `/etc/shadow`: password hashes, usually root-only.
- `/home`: user files.
- `/var/www`: common web root.
- `/opt`: third-party apps.
- `/tmp`: writable temporary files.
- `/etc/crontab`: scheduled jobs.

## Permissions

Read `ls -la` output:

```text
-rwxr-xr-x 1 user group 1234 file
```

- `r`: read.
- `w`: write.
- `x`: execute or enter directory.
- owner/group/other: three permission groups.
- SUID: execute as file owner; important for privesc.

## Shell Basics

After a shell:

```bash
python3 -c 'import pty; pty.spawn("/bin/bash")'
export TERM=xterm
stty rows 40 cols 120
```

Collect:

- current user and groups
- hostname and OS
- listening services
- credentials in app files
- sudo rules
- SUID/capabilities/cron

## When To Jump To Blueprints

- New machine target -> [Machine Exploit Blueprint](../blueprints/Machine%20Exploit%20Blueprint.md).
- Need a picker by signal -> [Machine Exploitation Databank](../blueprints/Machine%20Exploitation%20Databank.md).
- Linux shell landed -> [Linux Privilege Escalation Blueprint](../blueprints/machine-attacks/Linux%20Privilege%20Escalation%20Blueprint.md).
- Service-specific issue -> [Machine Attack Blueprint Index](../blueprints/machine-attacks/Machine%20Attack%20Blueprint%20Index.md).
