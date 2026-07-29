# Reversing CLI Tools Cheat Sheet

Command reference for the tools used across the reverse engineering playbook and local `rev_source` material.

## Fast Triage

```bash
file ./challenge
sha256sum ./challenge
strings -n 8 ./challenge | less
strings -n 8 -e l ./challenge | less
checksec --file ./challenge
binwalk ./challenge
```

Use this before running the file. Capture the file type, architecture, protections, strings, and embedded-file hints.

## Hex And Bytes

```bash
xxd ./challenge | head
xxd -g 1 -l 128 ./challenge
hexdump -C ./challenge | head
od -An -tx1 -v ./challenge | head
```

Patch with Python for repeatability:

```bash
python - <<'PY'
from pathlib import Path
p = Path("challenge")
data = bytearray(p.read_bytes())
data[0x1234:0x1236] = b"\x90\x90"
Path("challenge.patch").write_bytes(data)
PY
```

Small Vim hex edit:

```bash
vim -b challenge
:%!xxd
:%!xxd -r
:w challenge.patch
```

## ELF Inspection

```bash
readelf -h ./challenge
readelf -S ./challenge
readelf -s ./challenge | less
readelf -r ./challenge
readelf -d ./challenge
objdump -M intel -d ./challenge | less
objdump -M intel -D ./challenge | less
objdump -s -j .rodata ./challenge | less
nm -an ./challenge
ldd ./challenge
```

What to look for:

- symbols such as `main`, `win`, `check`, `validate`, `print_flag`
- `.rodata` constants and strings
- PLT/GOT imports such as `strcmp`, `memcmp`, `scanf`, `read`
- PIE/static/dynamic linking clues

## Runtime Tracing

```bash
strace -f ./challenge
strace -f -o strace.log ./challenge
ltrace ./challenge
ltrace -o ltrace.log ./challenge
```

Use `strace` for files, syscalls, process creation, and anti-debug behavior. Use `ltrace` for libc calls like `strcmp`, `strlen`, `memcmp`, and `printf`.

Useful filters:

```bash
strace -e trace=openat,read,write,execve ./challenge
strace -e trace=file ./challenge
```

## GDB

```bash
gdb -q ./challenge
gdb -q --args ./challenge arg1 arg2
gdb -q -batch -ex 'break main' -ex run -ex 'info registers' ./challenge
```

Open the full local sheet:

- [GDB (gef) Cheat Sheet](GDB%20Cheat%20Sheet.md)

## Radare2

```bash
r2 -A ./challenge
```

For the dedicated Rizin/Radare2 workflow and offline PDF source, open [Rizin / Radare2 Cheat Sheet](Rizin%20Radare2%20Cheat%20Sheet.md).

Inside r2:

```text
aaa
iI
afl
s main
pdf
iz
izz
axt @ sym.imp.strcmp
px 64 @ rsp
VV
q
```

Use r2 when you want a CLI-only function list, cross references, strings, and quick disassembly.

## ROP And Pwn Helpers

```bash
pwn checksec ./vuln
pwn cyclic 300
pwn cyclic -l 0x6161616c
ROPgadget --binary ./vuln | grep 'pop rdi'
ropper --file ./vuln --search 'pop rdi'
one_gadget libc.so.6
```

Use after confirming a memory corruption path.

## Python Bytecode

```bash
file challenge.pyc
python -m dis challenge.pyc
strings -n 8 challenge.pyc
```

PyInstaller:

```bash
python pyinstxtractor.py challenge.exe
python pyinstxtractor_ng.py challenge.exe
```

Try decompilers only after matching the Python version:

```bash
uncompyle6 module.pyc > module.py
decompyle3 module.pyc > module.py
```

When decompilation fails, read `dis` output and rebuild the logic manually.

## Java, APK, And .NET

```bash
jadx app.apk -d out
jadx-gui app.apk
javap -c -p ClassName.class
jar tf app.jar
```

.NET is usually easier in GUI tools:

- dnSpyEx
- ILSpy

Use CLI extraction first to inspect resources:

```bash
strings -n 8 app.exe | less
binwalk app.exe
```

## WebAssembly

```bash
file module.wasm
strings -n 8 module.wasm
wasm2wat module.wasm -o module.wat
wasm-decompile module.wasm > module.c
grep -n "export\\|memory\\|i32" module.wat
```

Look for exported validation functions, linear memory offsets, and expected byte arrays.

## Script And Payload Decoding

```bash
printf '%s' '68656c6c6f' | xxd -r -p
printf '%s' 'c2VjcmV0' | base64 -d
printf '%s' 'uryyb' | tr 'n-za-mN-ZA-M' 'a-mn-zA-MN-Z'
echo 'abc' | rev
```

OpenSSL staged payloads:

```bash
openssl enc -aes-256-cbc -base64 -d -pbkdf2 -k 'candidate-key' -in payload.b64 -out stage.bin
```

Clean XML workflow/script artifacts:

```bash
python - <<'PY'
from html import unescape
from pathlib import Path
text = Path("document.wflow").read_text(errors="ignore")
Path("document.decoded.txt").write_text(unescape(text))
PY
```

## Search And Text Processing

```bash
grep -Rni "flag\\|strcmp\\|memcmp\\|password" .
rg -n "flag|strcmp|memcmp|password"
sed -n '120,180p' file.txt
awk -F: '{print $1}' file.txt
sort file.txt | uniq -c | sort -nr
```

Use [Vim For Reversing Cheat Sheet](Vim%20For%20Reversing%20Cheat%20Sheet.md) for interactive cleanup and review.

## Visual / Bitmap Artifacts

```bash
file out.pbm
head out.pbm
xxd out.pbm | head
python -m pip install pillow
```

Use Python to parse PBM/bitmap rows and recover bit order; see [REV Python Toolkit](REV%20Python%20Toolkit.md#pbm--bitmap-bit-extraction).

## Tool Choice

| Need | Tool |
|---|---|
| identify file | `file`, `binwalk` |
| strings | `strings`, `rabin2 -zz`, FLOSS |
| ELF headers | `readelf` |
| disassembly | `objdump`, `r2`, Ghidra |
| debug ELF | GDB, pwndbg, GEF |
| trace files/syscalls | `strace` |
| trace libc calls | `ltrace` |
| patch bytes | Python, Vim+xxd, Ghidra/Scalpel |
| Python bytecode | `dis`, uncompyle/decompyle, PyLingual |
| Python decompiler | `pycdc`, `python-exe-unpacker` |
| APK/JAR / Android RE | `jadx`, `javap`, `apk.sh`, `Apktool`, `ReverseAPK` |
| JS deobfuscation | `synchrony` |
| Hex editing | `ImHex`, `hexedit`, Vim+xxd |
| Malware sandbox | `Limon`, `DRAKVUF Sandbox`, `Freki`, `Aleph` |
| Emulation / DBI | `qiling`, `QBDI` |
| WASM | WABT |
| constraints | Z3, NumPy |
| pwn | pwntools, ROPgadget, ropper |

## Related

- [Reverse Engineering Playbook](../Reverse%20Engineering%20Playbook.md)
- [IDA Pro Cheat Sheet](IDA%20Pro%20Cheat%20Sheet.md)
- [Ghidra Cheat Sheet](Ghidra%20Cheat%20Sheet.md)
- [x64dbg Cheat Sheet](x64dbg%20Cheat%20Sheet.md)
- [GDB (gef) Cheat Sheet](GDB%20Cheat%20Sheet.md)
- [Vim For Reversing Cheat Sheet](Vim%20For%20Reversing%20Cheat%20Sheet.md)
- [REV Python Toolkit](REV%20Python%20Toolkit.md)
