---
variants:
  - label: search-gadget
    command: |
      ROPgadget --binary $FILE | grep '$SEARCH'
  - label: ropper-search
    command: |
      ropper --file $FILE --search '$SEARCH'
description: Search for assembly instruction gadgets to build return-oriented programming (ROP) exploits.
os: [Linux]
category: [cli]
phase: [Exploitation]
references:
  - https://github.com/zernanvash/cheatsheet/blob/main/tools/Reversing%20CLI%20Tools%20Cheat%20Sheet.md
---
