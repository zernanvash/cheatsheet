# Rizin / Radare2 Cheat Sheet

Use this when you want CLI-first static analysis for ELF/PE binaries, quick function discovery, strings, XREFs, graph views, and patch planning without opening a full GUI decompiler.

Offline source PDF: [Rizin / Radare Cheat Sheet](../rev_source/rizin_radare_cheatsheet.pdf)

## When To Use

- You need fast terminal triage on a Linux VM.
- You want function lists, imports, sections, symbols, and strings without Ghidra/IDA.
- You are working over SSH or a slow remote desktop.
- You want to script analysis or inspect many binaries quickly.
- You need a second opinion before deeper work in Ghidra, IDA, GDB, or x64dbg.

Prefer Ghidra/IDA when you need a strong decompiler, type recovery, or large-project navigation. Prefer GDB/x64dbg when you need runtime state.

## First Pass

```bash
rizin -A ./challenge
r2 -A ./challenge
```

Inside Rizin/Radare2:

```text
aaa                 # analyze all
iI                  # binary info
ie                  # entrypoints
iS                  # sections
ii                  # imports
is                  # symbols
afl                 # functions
iz                  # strings in data sections
izz                 # strings from entire binary
q                   # quit
```

Use `rizin` when installed. Use `r2` when the box only has Radare2.

## Navigation

```text
s main              # seek to main
s sym.main          # seek to symbol
s 0x401000          # seek to address
pdf                 # print disassembly of current function
pdf @ main          # print main
pd 40               # disassemble 40 instructions
px 64               # hex dump 64 bytes
ps @ 0x402000       # print string at address
VV                  # visual graph mode
V!                  # panels mode in radare2
```

Useful visual mode keys:

```text
p                   # cycle visual print modes
g                   # go to address
u                   # undo seek
x                   # show xrefs
q                   # leave visual mode
```

## XREFs And Calls

```text
axt @ sym.imp.strcmp
axt @ str.Success
axt @ 0x402050
aflj                # function list as JSON
agf                 # function graph
agC                 # call graph
```

Common CTF pivots:

- XREF strings such as `Correct`, `Wrong`, `flag`, `password`, `Usage`.
- XREF imports such as `strcmp`, `memcmp`, `scanf`, `fgets`, `read`, `strstr`.
- Walk backward from success strings to the validation branch.

## Breakpoints With Debug Mode

Use debug mode only for scoped lab binaries you are allowed to run.

```bash
rizin -d ./challenge
r2 -d ./challenge
```

Inside:

```text
aaa
db main             # breakpoint
dc                  # continue
ds                  # step into
dso                 # step over
dr                  # registers
px 64 @ rsp         # stack bytes
ps @ rdi            # print string at rdi
dbt                 # backtrace
```

For heavy debugging, switch to [GDB (gef) Cheat Sheet](GDB%20Cheat%20Sheet.md) or [x64dbg Cheat Sheet](x64dbg%20Cheat%20Sheet.md).

## Patch Planning

Inspect candidate branch:

```text
pdf @ main
pd 12 @ 0x401234
```

Patch interactively only on a copy:

```bash
cp challenge challenge.patch
rizin -w challenge.patch
```

Inside:

```text
aaa
s 0x401234
wa nop              # assemble/write nop at seek
wa jmp 0x401260     # rewrite branch
wq                  # write and quit
```

For repeatability, record the offset and reproduce patches with Python.

## Quick Decision Table

| Signal | Command path |
|---|---|
| Need architecture/protections | `iI`, then confirm with `file` and `checksec` |
| Need function names | `aaa`, `afl` |
| Need strings | `iz`, `izz` |
| Need who references a string/import | `axt @ str.name`, `axt @ sym.imp.name` |
| Need validation logic | `s main`, `pdf`, then follow calls and conditional branches |
| Need graph view | `VV` or export `agf` |
| Need runtime registers | `rizin -d`, `db`, `dc`, `dr` |
| Need stable solver script | Extract constants and branches, then use [REV Python Toolkit](REV%20Python%20Toolkit.md) |

## Related

- [Reversing CLI Tools Cheat Sheet](Reversing%20CLI%20Tools%20Cheat%20Sheet.md)
- [Reverse Engineering Playbook](../Reverse%20Engineering%20Playbook.md)
- [GDB (gef) Cheat Sheet](GDB%20Cheat%20Sheet.md)
- [Ghidra Cheat Sheet](Ghidra%20Cheat%20Sheet.md)
- [IDA Pro Cheat Sheet](IDA%20Pro%20Cheat%20Sheet.md)
