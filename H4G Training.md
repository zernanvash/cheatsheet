# H4G Training CTF Playbook Hub

Welcome to the H4G Training Vault. This document serves as the navigation hub. Choose the playbook or guide matching your target type below.

---

## 🎯 Standard Environment Variables

Copy-paste this block into your terminal workspace before executing commands:

```bash
export TARGET="10.10.11.X"        # Target machine IP
export URL="http://10.10.11.X"     # Target base URL / endpoint
export LHOST="10.10.14.X"         # Attacker IP, usually tun0 / VPN interface
export LPORT="4444"               # Primary reverse shell listener port
export LPORT_ALT="4445"           # Secondary staging / shell listener port
```

---

## 🖥️ Machine Hacking & Boot2root
Comprehensive guides for exploiting networks, systems, and active directory boxes.
* **[Machine Exploitation Playbook](guides/Machine%20Exploitation%20Playbook.md)** — Core playbook covering Host/Port Recon, Initial Access, Shell Stabilization, Post-Exploitation, Linux/Windows Privilege Escalation, Lateral Movement, and File Transfers.
* **[Machine Exploitation Databank](blueprints/Machine%20Exploitation%20Databank.md)** — Exploit pathways and walkthrough mapping for known machines.
* **[Machine Attack Blueprint Index](blueprints/machine-attacks/Machine%20Attack%20Blueprint%20Index.md)** — Specific attack vectors (SMB, Kerberoasting, LFI, MSSQL, NFS, SNMP).

---

## 🌐 Web Exploitation
Solve templates and checklists for HTTP/web challenges.
* **[Web Exploitation Playbook](guides/Web%20Exploitation%20Playbook.md)** — Detailed syntax for SQL Injection (manual & SQLMap), Command Injection, LFI/RFI, Traversal, Upload Bypass, Auth Bypass, and API Testing.
* **[Web Exploit Blueprint](blueprints/Web%20Exploit%20Blueprint.md)** — Checklist for web applications and source review.

---

## ⚙️ Reverse Engineering & Pwn
Solve templates and disassemblers references.
* **[Reverse Engineering Playbook](Reverse%20Engineering%20Playbook.md)** — Standalone playbook for CPU registers, assembly priming, static vs dynamic analysis, and disassembler workflows.
* **[Reverse Engineering Blueprint](blueprints/Reverse%20Engineering%20Blueprint.md)** — APK/JAR, Python bytecode, WebAssembly, and solver scripts.
* **[Buffer Overflow Blueprint](blueprints/Buffer%20Overflow%20Blueprint.md)** — Stack vulnerabilities, ROP chains, and shellcode injections.
* **[REV Python Toolkit](tools/REV%20Python%20Toolkit.md)** — Python automation scripts.

---

## 🖼️ Steganography & Cryptography
Extracting hidden data and solving ciphers.
* **[Steganography Blueprint](blueprints/Steganography%20Blueprint.md)** — Analyzing hidden file metadata, embedded archives, audio spectrograms, and color channels.
* **[Cryptography Blueprint](blueprints/Cryptography%20Blueprint.md)** — Solvers for XOR ciphers, RSA public keys, and custom encodings.

---

## 🔑 Password Attacks
Identifying and cracking hashes.
* **[Password Attacks Playbook](guides/Password%20Attacks%20Playbook.md)** — Hashcat rules and cracking modes (NTLM, NTLMv2, Kerberoast, ASREP, md5, zip).

---

## 🛡️ Forensics & Incident Response
Packet analysis and event monitoring.
* **[Forensics and Blue Team Playbook](guides/Forensics%20and%20Blue%20Team%20Playbook.md)** — Wireshark/tshark packet filters, log analysis scripting (awk/uniq), and Sysmon rules.

---

## 📝 Reporting & Remediation
Documenting findings professionally.
* **[Reporting and Remediation Playbook](guides/Reporting%20and%20Remediation%20Playbook.md)** — Severity indicators, evidence templates, and remediation strategies.

---

## 🛠️ Indexes & Tools
* **[0xrefs Interactive Reference](0xrefs.html)** — Dynamic parameter cheatsheet with offline compatibility.
* **[Tools Index](tools/Tools%20Index.md)** — Quick access to specific command cheat sheets.
* **[References Index](references/References%20Index.md)** — Long-form source links and syscall tables.
* **[Learning Path Index](learning/Learning%20Path%20Index.md)** — Modular paths to learn the fundamentals first.
