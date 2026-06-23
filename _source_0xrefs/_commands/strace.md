---
variants:
  - label: trace-syscalls
    command: |
      strace -f -o strace.log ./$FILE
  - label: filter-files
    command: |
      strace -e trace=file ./$FILE
  - label: filter-specific
    command: |
      strace -e trace=openat,read,write,execve ./$FILE
description: Trace system calls, processes, and signals.
os: [Linux]
category: [cli]
phase: [Enumeration]
references:
  - https://github.com/zernanvash/cheatsheet/blob/main/tools/Reversing%20CLI%20Tools%20Cheat%20Sheet.md
---
