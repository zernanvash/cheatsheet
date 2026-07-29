# Reverse Engineering Blueprint

Workflow for CTF reversing, crackmes, byte transforms, VM-style programs, script malware, mobile apps, and WebAssembly-backed web challenges. This guide keeps writeup lessons generalized: use the patterns, not the original challenge-specific assumptions.

## 0. Pattern Selector

| Signal | Likely path | First action |
|---|---|---|
| readable flag check, constants, arrays, or encoded bytes | direct transform | Rebuild the check in Python and invert it. |
| PyInstaller, `.pyc`, or Python traceback strings | Python bytecode branch | Extract, identify Python version, decompile or disassemble. |
| Pyarmor markers or broken decompilation | protected Python | Prefer bytecode/disassembly and runtime-independent unpackers before execution. |
| anti-debug exit, self-delete, one-shot behavior | hostile runtime | Snapshot first, patch checks, or trace in batch mode. |
| many small state functions or indirect calls | state machine | Log transitions, count breakpoint hits, and recover state order. |
| custom bytecode, VM loop, `switch` dispatcher | VM lifting | Name opcodes, dump a trace, translate to Python/assembly, then solve the lifted logic. |
| large linear-looking math over flag bytes | matrix/constraints | Extract coefficients and solve with modular algebra, NumPy, or Z3. |
| graph transitions or path validation | graph solver | Extract edges and solve path/search constraints. |
| output is an image, PBM, bitmap, palette, or pixels | visual encoding | Recover row/column/bit mapping, then invert the image generation. |
| `Illegal instruction`, missing CPU feature, GUI-only app, or platform mismatch | static solve | Reimplement validation from constants and code; do not depend on local execution. |
| APK/JAR/.NET/Flutter/mobile bundle | managed/mobile branch | Decompile first, then inspect native libraries or framework-specific assets. |

## 0.1 Evidence Notebook

Track every challenge in this shape so you do not lose the route:

```text
File type:
Architecture/runtime:
Runs locally?:
Input length / format:
Success string:
Failure string:
State storage:
Important constants:
Transform hypothesis:
Solver path:
```

When a binary is dangerous, one-shot, self-deleting, or malware-like, copy it into a throwaway directory and work from a duplicate.

## 1. Triage

```bash
file ./challenge
strings -n 8 ./challenge
sha256sum ./challenge
checksec --file ./challenge
binwalk ./challenge
```

Branch quickly:

- script/source -> read and reproduce checks
- ELF/PE -> strings, disassembly, debugger
- APK/JAR -> Java decompile
- `.wasm` -> WABT tools
- crash after long input -> [Buffer Overflow Blueprint](Buffer%20Overflow%20Blueprint.md)
- packed binary -> unpack or debug runtime
- image-like output -> inspect generated file format and bit layout
- unsupported CPU/platform -> static reimplementation

## 2. First Execution

Run only in a disposable lab directory or VM.

```bash
chmod +x ./challenge
./challenge
ltrace ./challenge
strace -f ./challenge
```

Capture prompts, expected input length, error messages, and file/network access.

If the program changes local state, deletes itself, writes registry keys, creates launch agents, or only accepts one attempt, stop and switch to the hostile-runtime branch before running again.

## 3. Static Inspection

```bash
strings -n 8 ./challenge
objdump -d ./challenge | less
readelf -a ./challenge
rabin2 -I ./challenge
```

Look for constants, comparison functions, encoded blobs, suspicious loops, and imported crypto/string functions.

## 4. GDB Workflow

```bash
gdb ./challenge
break main
run
disassemble main
info registers
x/s 0xADDRESS
x/16xb 0xADDRESS
```

For picoCTF register tasks, break at the requested address and inspect the named register or memory address exactly as asked.

## 5. Assembly Patterns

Common patterns:

- `cmp` followed by conditional jump -> branch condition
- XOR/add/sub loops -> byte transform
- `strlen`/length compare -> expected length
- table lookup -> substitution or shuffle
- `strcmp`/`memcmp` -> direct expected bytes
- indirect calls through a table -> state machine or VM dispatch
- repeated multiply/add over input bytes -> matrix or linear equation
- division by a large constant/magic number -> compiler-optimized division or modulo
- bit shifts plus masks -> bitfield, pixel, nibble, or packed-state extraction

Use local references:

- [Guide to x86 Assembly](../references/Guide%20to%20x86%20Assembly.html)
- [Linux x86_64 syscall table](../references/Linux%20System%20Call%20Table%20for%20x86%2064%20-%20Ryan%20A.%20Chapman.html)

## 6. Hostile Runtime And Anti-Debug Branch

Use this when execution changes state, blocks debuggers, deletes files, phones home, asks for sensitive input, creates persistence, or gives only one try.

### Safe Handling

```bash
mkdir -p labcopy
cp ./challenge labcopy/challenge
sha256sum labcopy/challenge
strings -n 8 labcopy/challenge | tee labcopy/strings.txt
```

Prefer static analysis first. If you must run it, use a VM snapshot, no personal files, and captured network.

### Anti-Debug Signals

- Linux reads `/proc/self/status` and checks `TracerPid`.
- Calls to `ptrace`, `prctl`, `getppid`, timing checks, or busy debug-watch threads.
- Windows checks `IsDebuggerPresent`, `CheckRemoteDebuggerPresent`, `NtQueryInformationProcess`, registry state, or process names.
- Program exits only while attached to GDB/x64dbg.

Options:

```bash
strace -f ./challenge
ltrace ./challenge
gdb -q ./challenge
```

Patch or bypass:

- NOP the anti-debug call or force the branch that means "not debugged".
- Patch self-delete/destruction routines to return early.
- Delete or reset challenge-created state such as registry keys, config files, or marker files.
- Use batch-mode debugger scripts when the solve depends on breakpoint counts.

Batch GDB hit counter pattern:

```bash
gdb -q -batch \
  -ex 'break *0x401234' \
  -ex 'run AAAA' \
  -ex 'continue' \
  -ex 'continue' \
  ./challenge
```

Use this when success depends on how many times a state function, branch, or block is reached.

## 7. Linux Reverse Engineering Branch

Use this branch for ELF binaries, Linux crackmes, SUID binaries, pwn challenges, and Linux malware-style triage.

### Linux Triage

```bash
file ./challenge
checksec --file=./challenge
readelf -h ./challenge
readelf -s ./challenge | less
ldd ./challenge
strings -n 8 ./challenge
```

Decision points:

- dynamically linked ELF -> inspect libc calls with `ltrace`.
- syscalls or static binary -> inspect with `strace`, `objdump`, and GDB.
- SUID binary -> look for unsafe file access, command execution, environment trust, or memory corruption.
- crash after long input -> use [Buffer Overflow Blueprint](Buffer%20Overflow%20Blueprint.md).
- stripped binary -> rely on function boundaries, imports, strings, and debugger behavior.

### Linux Debugging

```bash
gdb ./challenge
break main
run
info functions
disassemble main
info registers
x/32gx $rsp
```

Useful runtime tracing:

```bash
ltrace ./challenge
strace -f ./challenge
```

### Linux Exploit-Reversing Notes

- Check `checksec` before picking a memory corruption path.
- For ret2win/ROP, identify function symbols, PLT/GOT entries, and useful gadgets.
- For SUID binaries, preserve environment assumptions and avoid destructive writes.
- For syscall-heavy binaries, keep the local syscall table open.

## 8. Windows Reverse Engineering Branch

Use this branch for PE files, Windows crackmes, .NET binaries, PowerShell droppers, DLLs, and Windows malware-style triage.

### Windows Triage

```powershell
Get-FileHash .\challenge.exe -Algorithm SHA256
```

Cross-platform checks:

```bash
file challenge.exe
strings -n 8 challenge.exe
```

Look for:

- PE architecture: x86 vs x64
- GUI vs console subsystem
- .NET metadata
- packed sections or high-entropy resources
- suspicious imports: `CreateProcess`, `WinExec`, `VirtualAlloc`, `WriteProcessMemory`, `LoadLibrary`, `GetProcAddress`
- config strings, URLs, mutexes, registry paths, and file paths

### Windows Static Tools

- Detect It Easy / PE-bear / CFF Explorer for PE structure.
- dnSpyEx or ILSpy for .NET.
- Ghidra, IDA Free, or Cutter for native PE disassembly.
- Resource Hacker for icons, dialogs, and embedded resources.
- FLOSS for decoded stack strings when available.

### Windows Debugging

- x64dbg for user-mode native debugging.
- WinDbg when you need lower-level exception, module, or symbol work.
- Process Monitor for file, registry, and process behavior.
- Process Explorer for process tree, handles, and loaded DLLs.

Common workflow:

1. Snapshot or isolate the VM.
2. Run static triage first.
3. Set breakpoints on validation functions, string compares, and suspicious APIs.
4. Inspect registers, stack, and memory around comparisons.
5. Patch locally only for analysis; keep original sample unchanged.

## 9. Script, Shell, And Payload Deobfuscation

Use this branch for shell scripts, Apple Automator/workflow files, PowerShell, batch, droppers, launch agents, mobileconfig/plist files, and staged payloads.

### Normalize Before Solving

```bash
file artifact
strings -n 6 artifact
xxd artifact | head
```

Common cleanup:

- XML entities: convert `&amp;`, `&gt;`, and `&lt;` back to shell syntax.
- Minified code: reformat before reasoning.
- Aliases/functions: resolve what commands really become.
- `tr`, `rev`, `xxd`, Base64, hex, ROT13: decode small pieces locally.
- Here-doc payloads: extract the body and decode/decrypt separately.
- Comments and filenames can be key material; do not delete them too early.
- Undefined variables often exist only to create visual noise.

Safe decode snippets:

```bash
printf '%s' '68656c6c6f' | xxd -r -p
printf '%s' 'uryyb' | tr 'n-za-mN-ZA-M' 'a-mn-zA-MN-Z'
printf '%s' 'c2VjcmV0' | base64 -d
```

OpenSSL payload shape:

```bash
openssl enc -aes-256-cbc -base64 -d -pbkdf2 -k 'candidate-key' -in payload.b64 -out stage.bin
```

For macOS persistence artifacts, inspect:

- `/Library/LaunchDaemons/*.plist`
- `/Library/LaunchAgents/*.plist`
- `/usr/local/bin/*`
- `.mobileconfig` XML keys and Base64 values
- firewall, `launchctl`, `mkfifo`, `nc`, `curl`, and exfiltration commands

## 10. Python Source, Bytecode, PyInstaller, And Pyarmor

For `.py`, `.pyc`, or PyInstaller:

```bash
file challenge
strings -n 8 challenge
pyinstxtractor.py challenge
python pyinstxtractor_ng.py challenge.exe
```

Use `dis` when source is bytecode-like:

```python
import dis

def check(value):
    return value[::-1] == "terces"

dis.dis(check)
```

Remove sleeps and failure exits in a local copy, then rebuild the validation transform instead of brute forcing blindly.

### PyInstaller Workflow

1. Detect with Detect It Easy, `file`, or PyInstaller strings.
2. Extract the bundle.
3. Identify likely entry point `.pyc`.
4. Match the Python bytecode version.
5. Try decompilers, but trust disassembly when decompilation is incomplete.

```bash
python -m dis module.pyc
strings -n 8 module.pyc
```

### Protected Python Workflow

If Pyarmor or another protector is present:

- Prefer offline/static unpackers if the script may be hostile.
- Read the accurate bytecode/disassembly even when generated source is broken.
- Remove protector prologue/epilogue noise mentally.
- Turn repeated bytecode blocks into small Python equivalents.
- Solve each independent validator separately, then combine parts.

Useful signs:

- `__pyarmor_enter_*`, `__pyarmor_exit_*`, `__pyarmor_assert_*`
- `pyarmor_runtime`
- decompiler warnings around new opcodes
- source that compiles but is semantically unreadable

## 11. Java, APK, .NET, Flutter, And Mobile

```bash
jadx-gui app.apk
jadx app.apk -d out
```

Review `MainActivity`, resources, hardcoded strings, native library loading, and validation methods.

Extra branches:

- JAR/class: use `jadx`, CFR, FernFlower, or Bytecode Viewer.
- Android native: inspect `lib/*.so` with Ghidra.
- .NET: use dnSpyEx or ILSpy, then inspect resources and config.
- Flutter: use `blutter` or framework-specific tooling, then inspect Dart snapshots and native libraries.
- Serialized/mobile assets: search resources, SQLite DBs, JSON, plist/XML, and bundled scripts.

## 12. WebAssembly

```bash
file module.wasm
strings -n 8 module.wasm
wasm2wat module.wasm -o module.wat
wasm-decompile module.wasm > module.c
```

Search exports, memory offsets, expected byte arrays, and simple transforms. Rebuild the check in Python.

## 13. Packed, Obfuscated, Or Unsupported Binaries

```bash
strings -n 8 ./challenge | grep -i upx
upx -d ./challenge
file ./challenge
```

If unpacking fails, debug after initialization and dump decrypted strings from memory.

If execution fails with `Illegal instruction`, missing CPU features, OS mismatch, or unavailable libraries:

- Stop trying to run it locally.
- Extract constants from the binary by offset, section, or decompiler view.
- Reimplement the validation logic in Python.
- Use emulation only when static reimplementation is too expensive.

## 14. Constraint, Matrix, And Algebra Branch

Use this when validation is many equations over flag bytes, repeated multiply/add loops, matrix multiplication, polynomial checks, or checksum-like constraints.

### Extraction Workflow

1. Find input length and printable range.
2. Locate encoded matrix/coefficient bytes and target bytes.
3. Decode obfuscated constants.
4. Write the exact math in Python.
5. Prefer direct algebra when obvious; use Z3 when the logic is mixed or modular.

Z3 modular byte skeleton:

```python
from z3 import BitVec, Solver, sat

SIZE = 64
matrix = [...]  # row-major coefficients
target = [...]

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

NumPy is better when the system is ordinary linear algebra over integers/reals and precision is under control:

```python
import numpy as np

A = np.array(coefficients, dtype=np.int64)
b = np.array(targets, dtype=np.int64)
x = np.linalg.lstsq(A, b, rcond=None)[0]
print(bytes(round(v) & 0xff for v in x))
```

Use `np.linalg.solve` for square invertible systems and `np.linalg.pinv` or `np.linalg.lstsq` for over/under-determined systems.

## 15. VM, State Machine, And Graph Branch

Use this when the binary implements its own instruction set, dispatch loop, state transition table, bytecode, graph traversal, or repeated state functions.

### VM Lifting Workflow

1. Identify the program counter, stack, memory, and dispatch variable.
2. Rename each opcode by behavior, not by guess.
3. Dump a trace: `pc`, opcode, operands, stack/memory effect.
4. Translate opcodes into Python or readable pseudo-assembly.
5. Remove unrelated runtime decoration and solve the lifted logic.

Trace shape:

```text
pc=1234 op=LOAD input[0]
pc=1235 op=PUSH 106
pc=1236 op=MUL
pc=1237 op=STORE tmp0
```

If the lifted program becomes equations, switch to the constraint branch. If it becomes transitions, build a graph.

### Graph Solver Pattern

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

This fits transition-table validators, Hamiltonian/Euler-style paths, maze state machines, and VM programs where input bytes select edges.

## 16. Visual, Bitmap, And Packed-Bit Branch

Use this when the program outputs an image, PBM/PGM/PPM, QR-like grid, palette data, pixels, or a visual artifact.

Workflow:

1. Identify the file header and dimensions.
2. Map loop index to row/column.
3. Find margins, repeated rows, and symmetry.
4. Recover bit order: LSB/MSB, row direction, column direction.
5. Strip padding/margins and rebuild bytes.

PBM/P1 parsing skeleton:

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

When decompiled code uses magic multiplication constants, test output patterns instead of getting stuck proving the optimization. A large multiply plus high-bit shift often represents division by a constant.

## 17. Solver Scripting

Use [REV Python Toolkit](../tools/REV%20Python%20Toolkit.md) for helpers. Minimal transform skeleton:

```python
expected = [0x20, 0x27, 0x23, 0x25]
plain = bytes(x ^ 0x42 for x in expected)
print(plain)
```

For constraints, use Z3; for path-heavy native binaries, consider angr.

## 18. Buffer Overflow Branch

Use [Buffer Overflow Blueprint](Buffer%20Overflow%20Blueprint.md) when a native binary crashes after long input, `checksec` shows exploitable mitigations, or the challenge category is `pwn` / `Binary Exploitation`.

Fast decision path:

1. Triage with `file`, `checksec`, `strings`, and first execution.
2. Confirm crash and find the offset with a cyclic pattern.
3. Decide between ret2win, shellcode, ret2libc, or ROP based on mitigations.
4. Build a repeatable pwntools script for local and remote solving.

## Tool And Reference Links

- [REV Python Toolkit](../tools/REV%20Python%20Toolkit.md)
- [Buffer Overflow Blueprint](Buffer%20Overflow%20Blueprint.md)
- [picoCTF Web and REV Patterns](../guides/picoCTF%20Web%20and%20REV%20Patterns.md)
- [REV references](../references/refernces.txt)
- [References Index](../references/References%20Index.md)
- [Local REV source inventory](../rev_source/README.md)

## Study Use Cases

- [GDB and assembly examples](../references/Challenge%20Use%20Cases.md#gdb-and-assembly)
- [Buffer overflow examples](../references/Challenge%20Use%20Cases.md#buffer-overflow)
- [Python solver scripting examples](../references/Challenge%20Use%20Cases.md#python-solver-scripting)
- [WebAssembly examples](../references/Challenge%20Use%20Cases.md#webassembly-checks)
