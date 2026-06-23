---
variants:
  - label: check-protections
    command: |
      checksec --file=$FILE
description: Verify binary security protections (NX, PIE, Canary, ASLR, RELRO).
os: [Linux]
category: [cli]
phase: [Enumeration]
references:
  - https://github.com/zernanvash/cheatsheet/blob/main/tools/Reversing%20CLI%20Tools%20Cheat%20Sheet.md
---
