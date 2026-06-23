---
variants:
  - label: scan
    command: |
      nmap --script smb-vuln-ms17-010 -p445 $IP
description: Scan for MS17-010 (EternalBlue) vulnerability in SMBv1.
os: [Linux]
category: [oscp]
service: [SMB]
phase: [Enumeration]
references:
  - https://github.com/zernanvash/cheatsheet/blob/main/tools/EternalBlue%20Cheat%20Sheet.md
---
