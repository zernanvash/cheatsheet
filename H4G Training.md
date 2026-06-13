# H4G Training

Start here. Pick the challenge type first, then open the smallest guide that matches what you are doing.

## Challenge Selector

| If the challenge is... | Open this first | Use when |
|---|---|---|
| Boot2root, HackMyVM, TryHackMe machine, OSCP-style box | [Machine Exploitation Databank](blueprints/Machine%20Exploitation%20Databank.md) | You have an IP or VM and need to choose the right attack path. |
| You already know the vulnerable service or attack type | [Machine Attack Blueprint Index](blueprints/machine-attacks/Machine%20Attack%20Blueprint%20Index.md) | You need a template such as SMB, Kerberoasting, LFI, upload, SSTI, MSSQL, NFS, SNMP, or privesc. |
| Web-only challenge or web foothold | [Web Exploit Blueprint](blueprints/Web%20Exploit%20Blueprint.md) | You are working with HTTP requests, routes, auth, sessions, upload, injection, or source review. |
| Binary, crackme, APK, Python bytecode, WebAssembly | [Reverse Engineering Blueprint](blueprints/Reverse%20Engineering%20Blueprint.md) | You need static/dynamic analysis, strings, GDB, decompilers, or solver scripting. |
| Native crash, pwn, ret2win, ret2libc, ROP | [Buffer Overflow Blueprint](blueprints/Buffer%20Overflow%20Blueprint.md) | A binary crashes with long input or the category is pwn/binary exploitation. |
| Hidden data in files, images, audio, metadata | [Steganography Blueprint](blueprints/Steganography%20Blueprint.md) | You have a suspicious artifact and need file/stego triage. |
| Encoding, ciphers, hashes, RSA, custom crypto | [Cryptography Blueprint](blueprints/Cryptography%20Blueprint.md) | You have ciphertext, keys, hashes, or crypto source code. |
| You do not understand the basics yet | [Learning Path Index](learning/Learning%20Path%20Index.md) | You need fundamentals before using a solve template. |

## Quick Study Routes

- Web beginner route: [Web Fundamentals](learning/Web%20Fundamentals.md) -> [Web Application Security Fundamentals](learning/Web%20Application%20Security%20Fundamentals.md) -> [Web Exploit Blueprint](blueprints/Web%20Exploit%20Blueprint.md)
- Machine beginner route: [Networking And Linux Fundamentals](learning/Networking%20And%20Linux%20Fundamentals.md) -> [Machine Exploitation Databank](blueprints/Machine%20Exploitation%20Databank.md) -> [Machine Exploit Blueprint](blueprints/Machine%20Exploit%20Blueprint.md)
- Windows/AD route: [Windows Fundamentals](learning/Windows%20Fundamentals.md) -> [Windows Privilege Escalation Blueprint](blueprints/machine-attacks/Windows%20Privilege%20Escalation%20Blueprint.md) -> [Active Directory Attack Path Cheat Sheet](tools/Active%20Directory%20Attack%20Path%20Cheat%20Sheet.md)
- Reversing route: [Reverse Engineering Fundamentals](learning/Reverse%20Engineering%20Fundamentals.md) -> [Reverse Engineering Blueprint](blueprints/Reverse%20Engineering%20Blueprint.md) -> [REV Python Toolkit](tools/REV%20Python%20Toolkit.md)
- Forensics/crypto route: [Steganography And Cryptography Fundamentals](learning/Steganography%20And%20Cryptography%20Fundamentals.md) -> [Steganography Blueprint](blueprints/Steganography%20Blueprint.md) or [Cryptography Blueprint](blueprints/Cryptography%20Blueprint.md)

## Indexes

- [Blueprint Index](blueprints/Blueprint%20Index.md) - all solve templates.
- [Learning Path Index](learning/Learning%20Path%20Index.md) - fundamentals and prerequisites.
- [Tools Index](tools/Tools%20Index.md) - command syntax and variants.
- [References Index](references/References%20Index.md) - offline sources, examples, and long-form notes.
- [Challenge Use Cases](references/Challenge%20Use%20Cases.md) - examples of when a technique appears in real CTF rooms.
