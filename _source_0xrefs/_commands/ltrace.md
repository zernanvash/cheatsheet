---
variants:
  - label: trace-libc
    command: |
      ltrace -o ltrace.log ./$FILE
description: Trace library calls (strcmp, strlen, memcmp, etc.) in dynamic binaries.
os: [Linux]
category: [cli]
phase: [Enumeration]
references:
  - https://github.com/zernanvash/cheatsheet/blob/main/tools/Reversing%20CLI%20Tools%20Cheat%20Sheet.md
---
