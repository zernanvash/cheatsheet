# OSCP Module Map

Local study map derived from the LeonardoE95 OSCP repository modules.

Source:

- https://github.com/LeonardoE95/OSCP/tree/main/modules
- https://github.com/LeonardoE95/OSCP

Use this page as a coverage checklist. Commands and local workflows are integrated into the H4G guides instead of requiring the remote repo during study.

## Web Module

Local guide: [Web Exploit Path](../guides/Web%20Exploit%20Path.md)  
Command sheet: [Web Testing](../tools/Web%20Testing.md)

Coverage:

- introduction to web exploitation
- Burp Suite request capture and replay
- SQL injection
- directory traversal
- local/remote file inclusion
- file upload vulnerabilities
- OS command injection
- cross-site scripting
- file and directory enumeration
- virtual host enumeration
- HTTP parameter enumeration
- brute force attacks
- DNS zone transfer attacks

Study order:

1. Baseline with `curl`, browser devtools, Burp, `whatweb`, and `nikto`.
2. Enumerate paths, files, extensions, virtual hosts, and parameters.
3. Review source leaks and request flows before using heavy scanners.
4. Test the core vulnerability classes manually, then automate confirmed paths.

## Linux Module

Local guide: [Linux Attack Path Cheat Sheet](../guides/Linux%20Attack%20Path%20Cheat%20Sheet.md)  
Main path: [Machine Exploit Path](../guides/Machine%20Exploit%20Path.md#5-linux-machine-branch)

Coverage:

- Linux shell basics
- file-system permissions
- Linux reverse shells
- PATH hijacking
- SUID exploitation
- sudo exploitation
- wildcard expansion exploitation
- system enumeration
- cron job enumeration
- capability enumeration
- local service exploitation
- Linux binary exploitation
- Linux kernel exploitation
- unshadow attack

Study order:

1. Enumerate identity, kernel, processes, sockets, sudo rules, cron, SUID, and capabilities.
2. Check credentials and application config before exploit paths.
3. Prefer misconfiguration routes before kernel exploits.
4. Use binary exploitation only when a custom SUID/native binary is clearly part of the challenge.

## Windows Module

Local guide: [Windows Attack Path Cheat Sheet](../guides/Windows%20Attack%20Path%20Cheat%20Sheet.md)  
Command sheet: [Windows Privilege Escalation Cheat Sheet](../tools/Windows%20Privilege%20Escalation%20Cheat%20Sheet.md)

Coverage:

- Windows shells
- Windows permissions
- Windows reverse shells
- cross compilation
- `SeImpersonatePrivilege`
- Windows services
- weak service permissions
- unquoted service paths
- DLL hijacking
- UAC bypass
- AlwaysInstallElevated
- sensitive files
- Windows hashes
- stored credentials
- critical registry paths
- scheduled tasks
- AMSI friction
- useful enumeration tools
- methodology and cheatsheet flow

Study order:

1. Enumerate identity, groups, privileges, OS/build, network, installed apps, services, tasks, and registry.
2. Hunt files, PowerShell history, KeePass, credential manager entries, and hashes.
3. Test service, scheduled task, registry, UAC, and token paths only when the preconditions match.

## Active Directory Module

Local guide: [Active Directory Attack Path Cheat Sheet](../tools/Active%20Directory%20Attack%20Path%20Cheat%20Sheet.md)

The upstream `modules/active-directory` directory currently contains only a placeholder, while the root README lists the intended topics:

- enumeration
- main tools
- Kerberoasting
- AS-REP roasting
- DCSync
- Mimikatz
- NTLM authentication
- Kerberos authentication

The local AD sheet already covers these plus BloodHound, LDAP, domain rights abuse, RBCD, ADCS, LAPS, gMSA, relay, and privileged group paths.

## Others Module

Local guide: [Post-Exploitation](../tools/Post-Exploitation.md)

The upstream README lists:

- port forwarding and pivoting
- using existing exploits
- client-side attacks

Local integration:

- SSH local/dynamic/remote forwarding in post-exploitation.
- exploit validation in machine exploitation and Metasploit sections.
- client-side attack reminders kept at a high level because weaponized document payloads are not needed for most CTF study paths.
