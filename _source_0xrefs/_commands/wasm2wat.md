---
variants:
  - label: convert-wat
    command: |
      wasm2wat $FILE -o module.wat
  - label: decompile
    command: |
      wasm-decompile $FILE > module.c
description: Convert WebAssembly to WebAssembly Text (WAT) or decompile to pseudo-C code.
os: [Linux]
category: [cli]
phase: [Enumeration]
references:
  - https://github.com/zernanvash/cheatsheet/blob/main/tools/Reversing%20CLI%20Tools%20Cheat%20Sheet.md
---
