# Forensics and Blue Team Playbook

# Standard Environment Variables
```bash
# Copy-paste this block into your terminal workspace before executing commands.
export TARGET="10.10.11.X"        # Target machine IP
export URL="http://10.10.11.X"     # Target base URL / endpoint
export LHOST="10.10.14.X"         # Attacker IP, usually tun0 / VPN interface
export LPORT="4444"               # Primary reverse shell listener port
export LPORT_ALT="4445"           # Secondary staging / shell listener port
```

---


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

[↑ Back to Table of Contents](#table-of-contents)

---



## Tool Reference

### Forensics Tools

Forensics Tools

- [Steganography Blueprint](../blueprints/Steganography%20Blueprint.md)
- [Cryptography Blueprint](../blueprints/Cryptography%20Blueprint.md)
- [REV Python Toolkit](../tools/REV%20Python%20Toolkit.md)



### Wordlists

Wordlists

```bash
ls /usr/share/wordlists
ls /usr/share/seclists
```

> **What to watch out for:** Match wordlists to the task: directory discovery, usernames, passwords, APIs, parameters, DNS, or fuzzing.



### External References

External References

- [Blueprint Index](../blueprints/Blueprint%20Index.md)
- [Learning Path Index](../learning/Learning%20Path%20Index.md)
- [Tools Index](../tools/Tools%20Index.md)
- [References Index](../references/References%20Index.md)
- [Challenge Use Cases](../references/Challenge%20Use%20Cases.md)

[↑ Back to Table of Contents](#table-of-contents)



---

[↑ Return to Hub](../H4G%20Training.md)
