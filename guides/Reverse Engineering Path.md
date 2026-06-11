# Reverse Engineering Path

Workflow for CTF reversing, crackmes, byte transforms, and WebAssembly-backed web challenges. Professor EH content did not include a dedicated reversing category, so this path stays grounded in local REV material and references.

## 1. Triage

```bash
file ./challenge
strings -n 8 ./challenge
sha256sum ./challenge
checksec --file ./challenge
```

Branch quickly:

- script/source -> read and reproduce checks
- ELF/PE -> strings, disassembly, debugger
- APK/JAR -> Java decompile
- `.wasm` -> WABT tools
- crash after long input -> [Buffer Overflow Guide](Buffer%20Overflow%20Guide.md)
- packed binary -> unpack or debug runtime

## 2. First Execution

Run only in a disposable lab directory or VM.

```bash
chmod +x ./challenge
./challenge
ltrace ./challenge
strace -f ./challenge
```

Capture prompts, expected input length, error messages, and file/network access.

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

Use local references:

- [Guide to x86 Assembly](../references/Guide%20to%20x86%20Assembly.html)
- [Linux x86_64 syscall table](../references/Linux%20System%20Call%20Table%20for%20x86%2064%20-%20Ryan%20A.%20Chapman.html)

## 6. Linux Reverse Engineering Branch

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
- crash after long input -> use [Buffer Overflow Guide](Buffer%20Overflow%20Guide.md).
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

## 7. Windows Reverse Engineering Branch

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

## 8. Python Source And Bytecode

For `.py`, `.pyc`, or PyInstaller:

```bash
file challenge
strings -n 8 challenge
pyinstxtractor.py challenge
```

Use `dis` when source is bytecode-like:

```python
import dis

def check(value):
    return value[::-1] == "terces"

dis.dis(check)
```

Remove sleeps and failure exits in a local copy, then rebuild the validation transform instead of brute forcing blindly.

## 9. Java And APK

```bash
jadx-gui app.apk
jadx app.apk -d out
```

Review `MainActivity`, resources, hardcoded strings, native library loading, and validation methods.

## 10. WebAssembly

```bash
file module.wasm
strings -n 8 module.wasm
wasm2wat module.wasm -o module.wat
wasm-decompile module.wasm > module.c
```

Search exports, memory offsets, expected byte arrays, and simple transforms. Rebuild the check in Python.

## 11. Packed Binaries

```bash
strings -n 8 ./challenge | grep -i upx
upx -d ./challenge
file ./challenge
```

If unpacking fails, debug after initialization and dump decrypted strings from memory.

## 12. Solver Scripting

Use [REV Python Toolkit](../tools/REV%20Python%20Toolkit.md) for helpers. Minimal transform skeleton:

```python
expected = [0x20, 0x27, 0x23, 0x25]
plain = bytes(x ^ 0x42 for x in expected)
print(plain)
```

For constraints, use Z3; for path-heavy native binaries, consider angr.

## 13. Buffer Overflow Branch

Use [Buffer Overflow Guide](Buffer%20Overflow%20Guide.md) when a native binary crashes after long input, `checksec` shows exploitable mitigations, or the challenge category is `pwn` / `Binary Exploitation`.

Fast decision path:

1. Triage with `file`, `checksec`, `strings`, and first execution.
2. Confirm crash and find the offset with a cyclic pattern.
3. Decide between ret2win, shellcode, ret2libc, or ROP based on mitigations.
4. Build a repeatable pwntools script for local and remote solving.

## Tool And Reference Links

- [REV Python Toolkit](../tools/REV%20Python%20Toolkit.md)
- [Buffer Overflow Guide](Buffer%20Overflow%20Guide.md)
- [picoCTF Web and REV Patterns](picoCTF%20Web%20and%20REV%20Patterns.md)
- [REV references](../references/refernces.txt)
- [References Index](../references/References%20Index.md)

## Study Use Cases

- [GDB and assembly examples](../references/Challenge%20Use%20Cases.md#gdb-and-assembly)
- [Buffer overflow examples](../references/Challenge%20Use%20Cases.md#buffer-overflow)
- [Python solver scripting examples](../references/Challenge%20Use%20Cases.md#python-solver-scripting)
- [WebAssembly examples](../references/Challenge%20Use%20Cases.md#webassembly-checks)
