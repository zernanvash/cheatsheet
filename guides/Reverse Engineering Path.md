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

## 6. Python Source And Bytecode

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

## 7. Java And APK

```bash
jadx-gui app.apk
jadx app.apk -d out
```

Review `MainActivity`, resources, hardcoded strings, native library loading, and validation methods.

## 8. WebAssembly

```bash
file module.wasm
strings -n 8 module.wasm
wasm2wat module.wasm -o module.wat
wasm-decompile module.wasm > module.c
```

Search exports, memory offsets, expected byte arrays, and simple transforms. Rebuild the check in Python.

## 9. Packed Binaries

```bash
strings -n 8 ./challenge | grep -i upx
upx -d ./challenge
file ./challenge
```

If unpacking fails, debug after initialization and dump decrypted strings from memory.

## 10. Solver Scripting

Use [REV Python Toolkit](../tools/REV%20Python%20Toolkit.md) for helpers. Minimal transform skeleton:

```python
expected = [0x20, 0x27, 0x23, 0x25]
plain = bytes(x ^ 0x42 for x in expected)
print(plain)
```

For constraints, use Z3; for path-heavy native binaries, consider angr.

## 11. Buffer Overflow Branch

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
