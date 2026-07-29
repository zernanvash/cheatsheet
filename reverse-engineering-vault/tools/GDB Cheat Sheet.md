# GDB (gef) Cheat Sheet

A comprehensive, production-grade GDB (GEF - GDB Enhanced Features) reference tailored for reverse engineers, malware analysts, and CTF players. Optimized for Linux ELF triaging, dynamic tracing, register inspection, and pwn/exploit development.

---

## 1. Starting GDB & GEF
GEF automatically colorizes and prints a multi-pane layout (Registers, Disassembly, Stack, Threads, Trace) on every stop.

```bash
gdb ./challenge                           # Start GDB
gdb -q ./challenge                        # Start in quiet mode (no banner)
gdb -q --args ./challenge arg1 arg2       # Start with command line arguments
```

### Passing Input inside GDB:
```gdb
run                                      # Run program
run < input.txt                          # Run with file redirected to stdin
run $(python -c 'print("A"*100)')        # Run with inline shell injection
set args arg1 arg2                       # Set arguments before running
show args                                # Display currently configured arguments
```

---

## 2. GEF Context & Screen Layout
GEF displays register values, disassembly around `RIP`, stack memory, and threads when execution halts.

* **`context`**: Force-redraw the GEF context pane layout.
* **`theme`**: Customize UI colors, symbols, and formatting.
* **`context Layout`**: Change which panes are shown.
  * *Example (hide trace & threads)*: `gef config context.layout "legend registers stack code source memory"`
* **TUI Mode**: Classic GDB text user interface (Warning: can clash with GEF styling):
  * `layout asm` / `layout regs`
  * `focus cmd` (switch keyboard input focus to command prompt)
  * `ctrl + x + a` (exit TUI mode)

---

## 3. Breakpoint Management

```gdb
break main                               # Break at main function symbol
break *0x401234                          # Break at raw address
break strcmp                             # Break at library import
info breakpoints                         # List all active breakpoints (shorthand: i b)
delete 1                                 # Delete breakpoint #1 (shorthand: d 1)
disable 1                                # Temporarily disable breakpoint #1
enable 1                                 # Enable breakpoint #1
```

### Conditional Breakpoints:
```gdb
break *0x401234 if $rax == 0x42          # Break only if RAX equals 0x42
break strcmp if $rdi == $rsi             # Break strcmp if comparison inputs are identical
```

### Command Hooks:
Execute GDB/GEF commands automatically whenever a breakpoint is hit:
```gdb
commands 1
  info registers
  telescope $rsp
  continue
end
```

---

## 4. Execution Flow Controls

| Command | Shorthand | Action |
|---|---|---|
| `run` | `r` | Start execution from the beginning. |
| `continue` | `c` | Continue running until next breakpoint or crash. |
| `stepi` | `si` | Step exactly one assembly instruction (enters calls). |
| `nexti` | `ni` | Step one assembly instruction (steps over/skips calls). |
| `finish` | `fin` | Run until the current function returns to its caller. |
| `until *0x401250`| | Run until execution reaches the specified address. |
| `kill` | `k` | Terminate the active debugging process. |

---

## 5. Register & Memory Manipulation

### Registers:
GEF colors changed registers in red and identifies memory pointers automatically.
```gdb
registers                                # Print all register values (GEF style)
print/x $rax                             # Print RAX in Hex
print/d $rax                             # Print RAX in Decimal
print/s $rax                             # Print RAX as a string pointer
set $rax = 0                             # Set register RAX to 0
set $rip = 0x401234                      # Force program execution pointer to another address
```

### Memory Patching:
```gdb
set {unsigned char}0x401234 = 0x90       # Patch a byte to NOP at address
set {unsigned char[2]}0x401234 = {0x90, 0x90} # Patch multiple bytes
set *0x401230 = 0xdeadbeef               # Write 32-bit integer to address
```

---

## 6. GEF-Specific Data Analysis Commands

### Telescope:
Recursively dereferences pointer chains at a target address (e.g., stack, registers).
```gdb
telescope $rsp                           # Dump stack with resolved pointer chains
telescope $rsp 20                        # Telescope stack 20 levels deep
telescope &global_var                    # Telescope a global pointer
```

### VMMap:
Lists virtual memory layout, section mappings, and permissions (Read/Write/Execute).
```gdb
vmmap                                    # Display full process memory mapping
vmmap libc                               # Filter map to libc allocations
```

### Pattern (Buffer Overflow Helper):
Create and parse cyclic patterns to identify stack offset overwrites.
```gdb
pattern create 128                       # Create a unique 128-byte cyclic pattern
pattern search 0x6161616c                # Find offset of value in pattern (e.g., from RIP)
pattern search $rsp                      # Automatically search RSP register offset
```

### Checksec:
```gdb
checksec                                 # Show binary protections (Canary, NX, PIE, ASLR)
```

### Stack Canary & GOT:
```gdb
canary                                   # Find stack canary location and current value
got                                      # Dump the Global Offset Table entries and resolve links
got strcmp                               # Check target resolved address for strcmp
```

### PIE (Position Independent Executables) helpers:
GEF tracks relative offsets when ASLR/PIE is active.
```gdb
pie breakpoint 0x1234                    # Set breakpoint at relative offset 0x1234
pie run                                  # Run program and offset relative addresses automatically
```

---

## 7. Memory Examination (Classic GDB `x`)
Format syntax: `x/[Count][Format][Size] [Address/Register]`

```gdb
x/s $rdi                                 # Examine RDI pointer as Null-terminated String
x/16xb 0x404000                          # Examine 16 hex bytes at address
x/8gx $rsp                               # Examine 8 Giant words (64-bit values) in hex at RSP
x/10i $rip                               # Examine 10 instructions starting at RIP
```

| Format Code | Meaning | Size Code | Meaning |
|---|---|---|---|
| **`x`** | Hexadecimal | **`b`** | Byte (8 bits) |
| **`d`** | Decimal (Signed) | **`h`** | Halfword (16 bits) |
| **`u`** | Decimal (Unsigned) | **`w`** | Word (32 bits) |
| **`s`** | String (null-terminated)| **`g`** | Giant word (64 bits) |
| **`i`** | Instruction | | |

---

## 8. Batch Mode Tracing (Automation)
Run GDB headlessly to automate checking comparison values or dump states.

```bash
# Break at strcmp and print comparison buffers
gdb -q -batch \
  -ex 'break strcmp' \
  -ex 'run' \
  -ex 'telescope $rdi' \
  -ex 'telescope $rsi' \
  ./challenge
```

---

## 9. Dynamic Anti-Debug Bypasses
If a program calls `ptrace` or checks `/proc/self/status` for `TracerPid`:

* **Catch Syscalls**:
  ```gdb
  catch syscall ptrace                   # Break when ptrace system call is invoked
  catch syscall openat                   # Break when status files are opened
  ```
* **Bypass logic**:
  1. Set breakpoint at the system call wrapper.
  2. Run program until breakpoint is triggered.
  3. Step out (`finish`) or query registers.
  4. Modify RAX (the return value) to indicate success:
     ```gdb
     set $rax = 0                        # Fake successful trace check
     ```

---

## Related Links
* [Reverse Engineering Playbook](../Reverse%20Engineering%20Playbook.md)
* [IDA Pro Cheat Sheet](IDA%20Pro%20Cheat%20Sheet.md)
* [Ghidra Cheat Sheet](Ghidra%20Cheat%20Sheet.md)
* [x64dbg Cheat Sheet](x64dbg%20Cheat%20Sheet.md)
