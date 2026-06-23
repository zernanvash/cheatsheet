---
variants:
  - label: mirror
    command: |
      wget -m ftp://anonymous:anonymous@$IP/
  - label: login
    command: |
      ftp $IP
  - label: crack
    command: |
      hydra -l $USER -P /usr/share/wordlists/rockyou.txt ftp://$IP
description: Mirror anonymous FTP, connect interactively, or password spray.
os: [Linux]
category: [oscp, cli]
service: [FTP]
phase: [Enumeration]
references:
  - https://github.com/zernanvash/cheatsheet/blob/main/tools/FTP%20Cheat%20Sheet.md
---
