---
variants:
  - label: headers
    command: |
      readelf -h $FILE
  - label: sections
    command: |
      readelf -S $FILE
  - label: symbols
    command: |
      readelf -s $FILE
  - label: imports
    command: |
      readelf -r $FILE
  - label: dynamic
    command: |
      readelf -d $FILE
description: Inspect ELF headers, sections, symbols, relocation table, or dynamic tags.
os: [Linux]
category: [cli]
phase: [Enumeration]
references:
  - https://github.com/zernanvash/cheatsheet/blob/main/tools/Reversing%20CLI%20Tools%20Cheat%20Sheet.md
---
