# GDB Cheat Sheet

Command-focused GDB reference for CTF reversing, crackmes, register questions, anti-debug checks, and pwn triage.

## Start

```bash
gdb ./challenge
gdb -q ./challenge
gdb -q --args ./challenge arg1 arg2
```

With input:

```gdb
run
run AAAA
run < input.txt
set args arg1 arg2
show args
```

## Breakpoints

```gdb
break main
break *0x401234
break strcmp
break memcmp
break puts
info breakpoints
delete 1
disable 1
enable 1
```

Conditional breakpoint:

```gdb
break *0x401234 if $rax == 0x42
```

Command block:

```gdb
commands
  info registers
  x/16xb $rsp
  continue
end
```

## Running And Stepping

```gdb
run
continue
stepi
nexti
finish
until
kill
quit
```

Use `stepi` to enter calls and `nexti` to step over calls.

## Registers

```gdb
info registers
info registers rax rbx rcx rdx rsi rdi rsp rbp rip
print/x $rax
print/d $rax
print/c $rax
set $rax = 0
set $rip = 0x401234
```

Common x86-64 Linux arguments:

| Argument | Register |
|---|---|
| 1 | `rdi` |
| 2 | `rsi` |
| 3 | `rdx` |
| 4 | `rcx` |
| 5 | `r8` |
| 6 | `r9` |
| return | `rax` |

## Memory Inspection

```gdb
x/s 0x404000
x/s $rdi
x/16xb 0x404000
x/16xw 0x404000
x/8gx $rsp
x/20i $rip
x/64cb $rsp
```

Formats:

| Format | Meaning |
|---|---|
| `x` | hex |
| `d` | signed decimal |
| `u` | unsigned decimal |
| `c` | char |
| `s` | string |
| `i` | instruction |
| `b` | byte |
| `h` | halfword |
| `w` | word |
| `g` | giant word / 8 bytes |

## Disassembly

```gdb
disassemble main
disassemble /r main
disassemble 0x401000,0x401080
info functions
info address main
```

Intel syntax:

```gdb
set disassembly-flavor intel
```

TUI:

```gdb
layout asm
layout regs
layout split
focus cmd
refresh
```

## Stack And Calls

```gdb
bt
frame 0
info frame
x/32gx $rsp
x/gx $rbp+8
```

Use this to find saved return addresses, local buffers, and call flow.

## Strings And Comparisons

Break on common validation calls:

```gdb
break strcmp
break strncmp
break memcmp
break strlen
run
```

At a string compare on Linux x86-64:

```gdb
x/s $rdi
x/s $rsi
```

At `memcmp`, inspect buffers and length:

```gdb
x/32xb $rdi
x/32xb $rsi
print/d $rdx
```

## Patching Runtime State

Patch register:

```gdb
set $eax = 0
set $rip = 0x401234
```

Patch memory byte:

```gdb
set {unsigned char}0x401234 = 0x90
```

Patch multiple bytes:

```gdb
set {unsigned char[2]}0x401234 = {0x90, 0x90}
```

Save patched memory range:

```gdb
dump memory patched.bin 0x400000 0x405000
```

## Anti-Debug Checks

Linux `TracerPid` / `ptrace` checks:

```gdb
catch syscall ptrace
catch syscall openat
catch syscall read
```

Common bypasses:

- patch the branch after the check
- force return value to success/failure as needed
- skip the call with `set $rip = ADDRESS_AFTER_CALL`
- use static patching for repeatability

## Batch Mode

```bash
gdb -q -batch \
  -ex 'set disassembly-flavor intel' \
  -ex 'break *0x401234' \
  -ex 'run AAAA' \
  -ex 'info registers' \
  -ex 'x/16xb $rsp' \
  ./challenge
```

Breakpoint hit counting:

```bash
gdb -q -batch \
  -ex 'break *0x401234' \
  -ex 'run input' \
  -ex 'continue' \
  -ex 'continue' \
  ./challenge
```

## Core Dumps

```bash
ulimit -c unlimited
./challenge
gdb ./challenge core
info registers
bt
```

## Pwndbg / GEF Useful Commands

Pwndbg:

```gdb
context
checksec
cyclic 200
cyclic -l 0x6161616c
vmmap
telescope $rsp
rop
```

GEF:

```gdb
context
checksec
pattern create 200
pattern offset 0x6161616c
vmmap
dereference $rsp
```

## Quick Workflows

Register question:

```gdb
break *0xADDRESS
run
info registers
```

Find expected string:

```gdb
break strcmp
run
x/s $rdi
x/s $rsi
```

Patch fail branch:

```gdb
disassemble main
break *0xFAIL_CHECK
run
set $rip = 0xSUCCESS_PATH
continue
```

Buffer overflow offset:

```bash
pwn cyclic 300 > pattern.txt
gdb ./vuln
run < pattern.txt
info registers
pwn cyclic -l 0xOVERWRITTEN
```

## Related

- [Reverse Engineering Playbook](../Reverse%20Engineering%20Playbook.md)
- [Reversing CLI Tools Cheat Sheet](Reversing%20CLI%20Tools%20Cheat%20Sheet.md)
- [REV Python Toolkit](REV%20Python%20Toolkit.md)
