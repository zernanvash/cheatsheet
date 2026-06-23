---
variants:
  - label: standard
    command: |
      dig $DOMAIN A
  - label: reverse
    command: |
      dig -x $IP
  - label: axfr
    command: |
      dig axfr $DOMAIN @$IP
  - label: trace
    command: |
      dig $DOMAIN +trace
description: DNS lookup, reverse lookup, trace recursion path, or request zone transfer using dig.
os: [Linux]
category: [oscp, cli]
service: [DNS]
phase: [Enumeration]
references:
  - https://github.com/zernanvash/cheatsheet/blob/main/tools/Dig%20Cheat%20Sheet.md
---
