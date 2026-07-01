# H4G Training CTF Playbook Hub

Welcome to the H4G Training Vault. Pick the **challenge category** you're working on and everything you need — playbooks, blueprints, cheatsheets, and learning paths — is grouped right there.

---

## 🎯 Quick Setup — Environment Variables

Copy-paste this block into your terminal before running any commands:

```bash
export TARGET="10.10.11.X"        # Target machine IP
export URL="http://10.10.11.X"     # Target base URL / endpoint
export LHOST="10.10.14.X"         # Attacker IP, usually tun0 / VPN interface
export LPORT="4444"               # Primary reverse shell listener port
export LPORT_ALT="4445"           # Secondary staging / shell listener port
```

---

## 🖥️ Machine Exploitation (Boot2Root / HackTheBox)

Full-scope machine hacking: recon, initial access, privilege escalation, lateral movement, and Active Directory.

### Playbooks & Blueprints
* **[Machine Exploitation Playbook](guides/Machine%20Exploitation%20Playbook.md)** — Core workflow: Host/Port Recon → Initial Access → Shell Stabilization → Post-Exploitation → PrivEsc → Lateral Movement → File Transfers.
* **[Machine Exploitation Databank](blueprints/Machine%20Exploitation%20Databank.md)** — Exploit pathways and walkthrough mapping for known machines.
* **[Machine Attack Blueprint Index](blueprints/machine-attacks/Machine%20Attack%20Blueprint%20Index.md)** — 40+ specific attack vectors (SMB, Kerberoasting, LFI, MSSQL, NFS, SNMP, Docker escape, etc.).

### Enumeration & Recon
* [Nmap Cheat Sheet](tools/Nmap%20Cheat%20Sheet.md) — Port scanning and service detection.
* [Footprinting Cheat Sheet](tools/Footprinting%20Cheat%20Sheet.md) — Host enumeration and fingerprinting.
* [Passive Recon](tools/Passive%20Recon.md) — OSINT, Whois, DNS, and public data gathering.
* [Dig Cheat Sheet](tools/Dig%20Cheat%20Sheet.md) — DNS zone queries and record lookup.
* [SMBClient Cheat Sheet](tools/SMBClient%20Cheat%20Sheet.md) — SMB share enumeration and file retrieval.
* [FTP Cheat Sheet](tools/FTP%20Cheat%20Sheet.md) — FTP login and file access.
* [SMTP](tools/SMTP.md) — Mail server user enumeration.
* [Networking](tools/Networking.md) — General networking commands and tunneling.
* [Service Enumeration Alternatives](tools/Service%20Enumeration%20Alternatives.md) — Advanced service scanning variants.
* [Cloud and Misc Recon Alternatives](tools/Cloud%20and%20Misc%20Recon%20Alternatives.md) — Cloud and non-standard recon.

### Exploitation & Initial Access
* [Metasploit](tools/Metasploit.md) — Framework usage and module selection.
* [EternalBlue Cheat Sheet](tools/EternalBlue%20Cheat%20Sheet.md) — MS17-010 exploitation.
* [Password Attacks](tools/Password%20Attacks.md) — Brute force, spraying, and credential stuffing.

### Privilege Escalation
* [Linux Attack Path Cheat Sheet](guides/Linux%20Attack%20Path%20Cheat%20Sheet.md) — Linux PrivEsc enumeration and exploit paths.
* [Windows Privilege Escalation Cheat Sheet](tools/Windows%20Privilege%20Escalation%20Cheat%20Sheet.md) — Windows PrivEsc vectors.
* [Windows Attack Path Cheat Sheet](guides/Windows%20Attack%20Path%20Cheat%20Sheet.md) — Full Windows attack chains.

### Active Directory
* [Active Directory Attack Path Cheat Sheet](tools/Active%20Directory%20Attack%20Path%20Cheat%20Sheet.md) — Full AD compromise workflow.
* [Kerberoasting Cheat Sheet](tools/Kerberoasting%20Cheat%20Sheet.md) — Service ticket cracking.
* [Pass-the-Hash Cheat Sheet](tools/Pass-the-Hash%20Cheat%20Sheet.md) — NTLM hash reuse.
* [Mimikatz Cheat Sheet](tools/Mimikatz%20Cheat%20Sheet.md) — Credential dumping.

### Post-Exploitation
* [Post-Exploitation](tools/Post-Exploitation.md) — Persistence, data exfiltration, and cleanup.

### Learning
* [Networking And Linux Fundamentals](learning/Networking%20And%20Linux%20Fundamentals.md)
* [Windows Fundamentals](learning/Windows%20Fundamentals.md)
* [Red Team Fundamentals](learning/Red%20Team%20Fundamentals.md)

---

## 🌐 Web Exploitation

SQL injection, XSS, command injection, LFI/RFI, SSRF, upload bypass, API testing, and source code review.

### Playbooks & Blueprints
* **[Web Exploitation Playbook](guides/Web%20Exploitation%20Playbook.md)** — Detailed syntax for SQLi (manual & SQLMap), Command Injection, LFI/RFI, Traversal, Upload Bypass, Auth Bypass, and API Testing.
* **[Web Exploit Blueprint](blueprints/Web%20Exploit%20Blueprint.md)** — Checklist-driven web app assessment and source review workflow.

### Cheatsheets
* [Web Testing](tools/Web%20Testing.md) — Burp Suite, directory busting, parameter fuzzing.
* [Web Attack Alternatives](tools/Web%20Attack%20Alternatives.md) — Advanced web attack variants and edge cases.
* [picoCTF Web and REV Patterns](guides/picoCTF%20Web%20and%20REV%20Patterns.md) — Common CTF web challenge patterns.

### Learning
* [Web Fundamentals](learning/Web%20Fundamentals.md)
* [Web Application Security Fundamentals](learning/Web%20Application%20Security%20Fundamentals.md)

---

## ⚙️ Reverse Engineering (REV)

Static and dynamic analysis of compiled binaries, bytecode, managed code, and obfuscated payloads.

### Playbooks & Blueprints
* **[Reverse Engineering Playbook](Reverse%20Engineering%20Playbook.md)** — Full standalone playbook: CPU registers, assembly primer, control flow patterns, static vs dynamic analysis, solver cookbook (XOR, Z3, angr, matrix), and tool reference.
* **[Reverse Engineering Blueprint](blueprints/Reverse%20Engineering%20Blueprint.md)** — Decision-tree workflow for ELF, PE, APK/JAR, Python bytecode, WebAssembly, and exotic targets.
* **[Reverse Engineering Tool Workflow](guides/Reverse%20Engineering%20Tool%20Workflow.md)** - Situation-driven tool selection for Kali plus Windows-host PE challenge workflows, based on the NTHW reverse engineering tool catalog.

### Disassembler Cheatsheets (Static Analysis)
* [IDA Pro Cheat Sheet](tools/IDA%20Pro%20Cheat%20Sheet.md) — Navigation, XREFs, type refactoring, structures, patching, and IDAPython.
* [Ghidra Cheat Sheet](tools/Ghidra%20Cheat%20Sheet.md) — Equivalent workflows, Data Type Manager, structures, and Jython scripting.
* [Reversing CLI Tools Cheat Sheet](tools/Reversing%20CLI%20Tools%20Cheat%20Sheet.md) — `file`, `strings`, `readelf`, `objdump`, `strace`, `ltrace`, `r2`, WABT, and PyInstaller extraction.

### Debugger Cheatsheets (Dynamic Analysis)
* [GDB (gef) Cheat Sheet](tools/GDB%20Cheat%20Sheet.md) — GEF context views, telescope, vmmap, pattern tools, anti-debug bypasses, and batch automation.
* [x64dbg Cheat Sheet](tools/x64dbg%20Cheat%20Sheet.md) — Windows PE debugging, memory dumps, hardware breakpoints, patching, and Scylla unpacking.

### Solver & Scripting
* [REV Python Toolkit](tools/REV%20Python%20Toolkit.md) — Python solvers for XOR, Z3, matrix systems, VM traces, graph paths, bytecode, and PBM extraction.
* [Vim For Reversing Cheat Sheet](tools/Vim%20For%20Reversing%20Cheat%20Sheet.md) — Hex editing, dump cleanup, and text processing.
* [picoCTF Web and REV Patterns](guides/picoCTF%20Web%20and%20REV%20Patterns.md) — Common CTF reversing patterns and solve strategies.

### 🎯 Practice
* **[Exercises & Practice Hub](Exercises.md)** — All hands-on exercises across every category in one place.
* **[REV Practice — crackmes.one CTF 2026](REV%20Practice.md)** — 12 challenges arranged by difficulty (Warm-Up → Expert) with descriptions, checklist, and optional hints.
* **[IDA Z3 Crackmes Hub (Browser)](rev_source/z3_practice.html)** — 20 interactive pseudo-C constraint-solving challenges spanning Easy, Medium, and Hard tiers.

### Learning
* [Reverse Engineering Fundamentals](learning/Reverse%20Engineering%20Fundamentals.md)

---

## 💥 PWN (Binary Exploitation)

Stack overflows, buffer overflows, ROP chains, ret2libc, shellcode injection, and format strings.

### Blueprints
* **[Buffer Overflow Blueprint](blueprints/Buffer%20Overflow%20Blueprint.md)** — Full workflow: checksec triage, offset discovery, ret2win, ret2libc, ROP chains, and remote exploit templates.
* **[Reverse Engineering Playbook — BOF Section](Reverse%20Engineering%20Playbook.md#buffer-overflow-quick-reference)** — Inline quick reference for buffer overflow challenges.

### Cheatsheets
* [GDB (gef) Cheat Sheet](tools/GDB%20Cheat%20Sheet.md) — Breakpoints, pattern create/search, canary detection, GOT inspection, PIE helpers.
* [Reversing CLI Tools Cheat Sheet](tools/Reversing%20CLI%20Tools%20Cheat%20Sheet.md) — `checksec`, `ROPgadget`, `ropper`, `one_gadget`, `pwntools`.
* [REV Python Toolkit](tools/REV%20Python%20Toolkit.md) — Pwntools exploit templates and helpers.

### Learning
* [Reverse Engineering Fundamentals](learning/Reverse%20Engineering%20Fundamentals.md) — Covers stack, calling conventions, and memory layout.

---

## 🛡️ Forensics & Incident Response

Packet analysis, log analysis, memory forensics, and event monitoring.

### Playbooks
* **[Forensics and Blue Team Playbook](guides/Forensics%20and%20Blue%20Team%20Playbook.md)** — Wireshark/tshark packet filters, log analysis scripting (awk/uniq), and Sysmon rules.

### Cheatsheets
* [Linux Text Processing](tools/Linux%20Text%20Processing.md) — `grep`, `awk`, `sed`, `sort`, `uniq` for log and artifact processing.

---

## 🖼️ Steganography

Extracting hidden data from images, audio, archives, and metadata.

### Blueprints
* **[Steganography Blueprint](blueprints/Steganography%20Blueprint.md)** — Analyzing hidden file metadata, embedded archives, audio spectrograms, and color channels.

### Learning
* [Steganography And Cryptography Fundamentals](learning/Steganography%20And%20Cryptography%20Fundamentals.md)

---

## 🔐 Cryptography

Solving ciphers, breaking encodings, and cracking hashes.

### Blueprints
* **[Cryptography Blueprint](blueprints/Cryptography%20Blueprint.md)** — Solvers for XOR ciphers, RSA public keys, and custom encodings.

### Cheatsheets
* [Password Attacks Playbook](guides/Password%20Attacks%20Playbook.md) — Hashcat rules and cracking modes (NTLM, NTLMv2, Kerberoast, ASREP, md5, zip).

### Learning
* [Steganography And Cryptography Fundamentals](learning/Steganography%20And%20Cryptography%20Fundamentals.md)
* [Crypto101 — Full Textbook](learning/Crypto101.md) — Crypto 101 by lvh: XOR, AES, stream ciphers, RSA, hash functions, MACs, TLS, GPG, OTR, and more (CC BY-NC 4.0).

---

## 🔍 OSINT

Open-source intelligence gathering and passive reconnaissance.

### Cheatsheets
* [Passive Recon](tools/Passive%20Recon.md) — Whois, DNS, Google dorking, Shodan, and public data sources.
* [Dig Cheat Sheet](tools/Dig%20Cheat%20Sheet.md) — DNS record queries and zone transfers.
* [Cloud and Misc Recon Alternatives](tools/Cloud%20and%20Misc%20Recon%20Alternatives.md) — Cloud-specific and non-standard recon.

---

## 📝 Reporting & Remediation

Documenting findings professionally.
* **[Reporting and Remediation Playbook](guides/Reporting%20and%20Remediation%20Playbook.md)** — Severity indicators, evidence templates, and remediation strategies.

---

## 🛠️ Cross-Cutting Resources

* **[Exercises & Practice Hub](Exercises.md)** — All hands-on exercises, interactive crackmes, and CTF practice sets.
* **[0xrefs Interactive Reference](0xrefs.html)** — Dynamic parameter cheatsheet with search, filter, and offline compatibility.
* **[Tools Index](tools/Tools%20Index.md)** — All cheatsheets organized by CTF category.
* **[References Index](references/References%20Index.md)** — Long-form source links, syscall tables, and external documentation.
* **[Learning Path Index](learning/Learning%20Path%20Index.md)** — Modular paths to learn the fundamentals first.
* **[Challenge Use Cases](references/Challenge%20Use%20Cases.md)** — Worked examples across multiple challenge types.
