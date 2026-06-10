# REV Python Toolkit

Common Python helpers for reverse engineering, crackmes, binary parsing, byte conversion, XOR, crypto checks, symbolic solving, and angr workflows.

Reference analyzed: `hgbe02/Hackmyvm-HMVLabs-Temperance`, a set of Python solvers for HackMyVM Temperance levels using `pwntools`, encoding transforms, image parsing, hashing, OCR, QR decoding, ZIP parsing, HTTP parsing, and XOR.

## Core Libraries

- `bytes`, `bytearray`, `memoryview` - raw byte handling
- `struct` - pack/unpack binary integers and records
- `binascii` - hex/base64 helpers
- `base64` - Base64/Base32/Base85
- `hashlib` - MD5/SHA family
- `hmac` - keyed hashes
- `itertools` - permutations, combinations, product brute force
- `io` - in-memory file objects
- `zipfile` - ZIP parsing in memory
- `requests` - HTTP fetch/parse automation
- `PIL.Image` from `pillow` - image inspection
- `pytesseract` - OCR for image text
- `pyzbar` - QR/barcode decoding
- `Crypto.Cipher` from `pycryptodome` - AES/DES/ARC4/etc.
- `z3` - symbolic constraints
- `angr` - binary symbolic execution
- `capstone` - disassembly
- `keystone` - assembly
- `unicorn` - CPU emulation
- `lief` - PE/ELF/Mach-O parsing and patching
- `pefile` - PE parsing
- `elftools` - ELF parsing
- `pwntools` - packing, tubes, ELF helpers

Install common stack:

```bash
python -m pip install pycryptodome z3-solver angr capstone keystone-engine unicorn lief pefile pyelftools pwntools
```

For image/OCR/QR challenge automation:

```bash
python -m pip install pillow pytesseract pyzbar requests
```

Tesseract OCR also needs the system package installed.

## Remote Challenge Template

Pattern from the Temperance solvers: connect, receive challenge, transform, send answer.

```python
from pwn import remote, log

HOST = "example.ctf.local"
PORT = 31337

s = remote(HOST, PORT)
banner = s.recv(1024)
log.info(banner.decode(errors="ignore"))

s.sendline(b"level-name")
challenge = s.recv(4096).strip()

answer = challenge  # replace with transform
s.sendline(answer if isinstance(answer, bytes) else str(answer).encode())

print(s.recv(4096).decode(errors="ignore"))
s.close()
```

Helpers for noisy services:

```python
line = s.recvline().strip()
s.recvuntil(b"Input: ")
s.sendline(b"answer")
```

## Bytes And Encoding

```python
data = b"ABC"
print(data.hex())
print(bytes.fromhex("414243"))
print(list(data))
print(data[::-1])
```

String to bytes:

```python
s = "hello"
b = s.encode()
print(b)
print(b.decode())
```

Integer conversions:

```python
n = 0x41424344
print(n.to_bytes(4, "big"))
print(n.to_bytes(4, "little"))
print(int.from_bytes(b"ABCD", "big"))
print(int.from_bytes(b"ABCD", "little"))
```

## struct Pack / Unpack

```python
import struct

buf = struct.pack("<I", 0x41424344)
print(buf)
print(struct.unpack("<I", buf)[0])
```

Formats:

- `<` little endian
- `>` big endian
- `B` uint8
- `H` uint16
- `I` uint32
- `Q` uint64

## Base Encodings

```python
import base64

raw = b"secret"
print(base64.b64encode(raw))
print(base64.b64decode(b"c2VjcmV0"))
print(base64.b32encode(raw))
print(base64.b85encode(raw))
```

Hex decode:

```python
print(bytes.fromhex("666c6167"))
print(b"flag".hex())
```

Decimal bytes to text:

```python
nums = "102 108 97 103".split()
print("".join(chr(int(n)) for n in nums))
```

## XOR Helpers

Single-byte XOR:

```python
def xor_byte(data, key):
    return bytes(b ^ key for b in data)

ct = bytes.fromhex("2b272e2e2d")
for k in range(256):
    pt = xor_byte(ct, k)
    if all(32 <= c < 127 for c in pt):
        print(k, pt)
```

Repeating-key XOR:

```python
def xor_key(data, key):
    key = key if isinstance(key, bytes) else key.encode()
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))

print(xor_key(b"hello", b"key"))
```

Repeating-key XOR for string challenges:

```python
def xor_text(text, key):
    return "".join(chr(ord(ch) ^ ord(key[i % len(key)])) for i, ch in enumerate(text))

print(xor_text("ciphertext", "HMV"))
```

Known-plaintext key recovery:

```python
ct = bytes.fromhex("0011223344")
known = b"flag{"
key_stream = bytes(c ^ p for c, p in zip(ct, known))
print(key_stream.hex())
```

## Hashing

```python
import hashlib

data = b"password"
print(hashlib.md5(data).hexdigest())
print(hashlib.sha1(data).hexdigest())
print(hashlib.sha256(data).hexdigest())
```

Wordlist check:

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

Permutation brute force against an MD5:

```python
import hashlib
import itertools

target = "md5_here"
chars = "abc123"

for perm in itertools.permutations(chars):
    candidate = "".join(perm)
    if hashlib.md5(candidate.encode()).hexdigest() == target:
        print(candidate)
        break
```

Cartesian brute force for fixed charset/length:

```python
import itertools

charset = "abcdef012345"
for tup in itertools.product(charset, repeat=4):
    candidate = "".join(tup)
    # test candidate
```

## Morse

```python
MORSE = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.",
    "G": "--.", "H": "....", "I": "..", "J": ".---", "K": "-.-", "L": ".-..",
    "M": "--", "N": "-.", "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.",
    "S": "...", "T": "-", "U": "..-", "V": "...-", "W": ".--", "X": "-..-",
    "Y": "-.--", "Z": "--..", "0": "-----", "1": ".----", "2": "..---",
    "3": "...--", "4": "....-", "5": ".....", "6": "-....", "7": "--...",
    "8": "---..", "9": "----."
}

REV_MORSE = {v: k for k, v in MORSE.items()}
msg = ".-- ...- .-. --.."
print("".join(REV_MORSE[x] for x in msg.split()))
```

## AES With PyCryptodome

```python
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

key = b"A" * 16
iv = b"B" * 16
pt = b"message"

cipher = AES.new(key, AES.MODE_CBC, iv)
ct = cipher.encrypt(pad(pt, 16))

cipher = AES.new(key, AES.MODE_CBC, iv)
print(unpad(cipher.decrypt(ct), 16))
```

ECB check:

```python
blocks = [ct[i:i+16] for i in range(0, len(ct), 16)]
print(len(blocks) != len(set(blocks)))
```

## ROT And Caesar

```python
import codecs

print(codecs.decode("synt", "rot_13"))
```

Caesar brute force:

```python
import string

alpha = string.ascii_lowercase
text = "uryyb"
for shift in range(26):
    out = "".join(alpha[(alpha.index(c) - shift) % 26] if c in alpha else c for c in text)
    print(shift, out)
```

## Binary File Helpers

Read file:

```python
from pathlib import Path

data = Path("sample.bin").read_bytes()
print(len(data), data[:16].hex())
```

Patch bytes:

```python
from pathlib import Path

data = bytearray(Path("sample.bin").read_bytes())
data[0x100:0x104] = b"\x90\x90\x90\x90"
Path("patched.bin").write_bytes(data)
```

Find strings:

```python
import re
from pathlib import Path

data = Path("sample.bin").read_bytes()
for s in re.findall(rb"[ -~]{4,}", data):
    print(s.decode(errors="ignore"))
```

## In-Memory ZIP

Useful when a service sends a Base64 ZIP and expects the content of the first file.

```python
import base64
import io
import zipfile

blob = base64.b64decode(challenge)
zf = zipfile.ZipFile(io.BytesIO(blob))
name = zf.namelist()[0]
content = zf.read(name)
print(content.decode(errors="ignore"))
```

## Images From Base64

Open an image without writing it to disk:

```python
import base64
import io
from PIL import Image

blob = base64.b64decode(challenge)
img = Image.open(io.BytesIO(blob))
print(img.size)
print(img.mode)
```

Read pixels:

```python
pixels = img.load()
print(pixels[0, 0])

for x in range(img.width):
    r, g, b, *rest = pixels[x, 0]
    alpha = rest[0] if rest else None
```

Extract text from RGBA alpha values:

```python
out = []
for x in range(img.width):
    px = img.getpixel((x, 0))
    if len(px) == 4:
        out.append(chr(px[3]))
print("".join(out))
```

## OCR

```python
import base64
import io
from PIL import Image
import pytesseract

img = Image.open(io.BytesIO(base64.b64decode(challenge)))
text = pytesseract.image_to_string(img).strip()
print(text)
```

If OCR is noisy, preprocess:

```python
img = img.convert("L")
img = img.point(lambda p: 255 if p > 160 else 0)
```

## QR Decode

```python
import base64
import io
from PIL import Image
import pyzbar.pyzbar as pyzbar

img = Image.open(io.BytesIO(base64.b64decode(challenge)))
decoded = pyzbar.decode(img)
print("".join(d.data.decode() for d in decoded))
```

## HTTP Parsing Automation

Fetch a URL from a challenge and extract a field from `/etc/passwd` style content:

```python
import requests

url = challenge.decode().strip()
body = requests.get(url, timeout=10).text

for line in body.splitlines():
    parts = line.split(":")
    if len(parts) > 2 and parts[0] == "proxy":
        print(parts[2])
```

## Z3 Basics

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

Byte constraints:

```python
from z3 import *

chars = [BitVec(f"c{i}", 8) for i in range(4)]
s = Solver()
for c in chars:
    s.add(c >= 0x20, c <= 0x7e)
s.add(chars[0] ^ chars[1] == 0x10)
s.add(chars[2] + chars[3] == 150)

if s.check() == sat:
    m = s.model()
    print(bytes([m[c].as_long() for c in chars]))
```

## angr Skeleton

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

Symbolic stdin:

```python
import angr
import claripy

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

## Capstone Disassembly

```python
from capstone import *

code = bytes.fromhex("554889e5")
md = Cs(CS_ARCH_X86, CS_MODE_64)
for insn in md.disasm(code, 0x1000):
    print(hex(insn.address), insn.mnemonic, insn.op_str)
```

## Keystone Assembly

```python
from keystone import *

ks = Ks(KS_ARCH_X86, KS_MODE_64)
encoding, count = ks.asm("xor eax, eax; ret")
print(bytes(encoding).hex())
```

## PE / ELF Quick Checks

PE:

```python
import pefile

pe = pefile.PE("sample.exe")
print(hex(pe.OPTIONAL_HEADER.ImageBase))
for section in pe.sections:
    print(section.Name, hex(section.VirtualAddress), hex(section.Misc_VirtualSize))
```

ELF:

```python
from elftools.elf.elffile import ELFFile

with open("sample", "rb") as f:
    elf = ELFFile(f)
    print(elf.header["e_machine"])
    for sec in elf.iter_sections():
        print(sec.name, hex(sec["sh_addr"]))
```

## pyc / PyInstaller

Common tools:

- `pyinstxtractor.py` - extract PyInstaller bundles
- `uncompyle6`, `decompyle3`, or PyLingual - decompile Python bytecode when supported

Flow:

1. Identify with `file`.
2. Extract with PyInstaller extractor if bundled.
3. Match Python version.
4. Decompile `.pyc`.
5. Read constants with `strings` or `dis` when decompile fails.

Python `dis`:

```python
import dis

def check(x):
    return x[::-1] == "terces"

dis.dis(check)
```

## picoCTF REV Patterns

Integrated from `Cajac/picoCTF-Writeups`. These are common CTF reverse engineering branches, especially useful before reaching for heavier tools.

### First Triage Commands

```bash
file ./challenge
strings -n 8 ./challenge
chmod +x ./challenge
./challenge
objdump -d ./challenge | less
```

Branch quickly:

- obvious strings -> validate and submit
- register/address question -> use GDB
- Python source -> patch or reproduce checks
- Java/APK -> decompile with jadx
- WebAssembly -> use WABT tools
- sparse strings or UPX marker -> unpack first

### GDB Register And Memory Tasks

```bash
gdb ./challenge
layout asm
break *main
run
info registers
x/s 0xADDRESS
x/16xb 0xADDRESS
disassemble main
```

For picoCTF baby-step style tasks, set a breakpoint at the requested address, run to it, then inspect the named register or memory address. Convert decimal, hex, or ASCII exactly as requested by the prompt.

### Byte Transform Solver Skeleton

Use for XOR, addition/subtraction, index shuffles, and simple flag validation loops.

```python
def transform(data):
    out = bytearray()
    for i, b in enumerate(data):
        out.append((b ^ 0x42) & 0xff)
    return bytes(out)

candidate = bytes.fromhex("001122334455")
print(transform(candidate))
```

Index shuffle pattern:

```python
data = b"example_flag_order"
order = [3, 0, 1, 2]
print(bytes(data[i] for i in order))
```

Reverse a check that stores expected transformed bytes:

```python
expected = [0x20, 0x27, 0x23, 0x25]
plain = bytes(x ^ 0x42 for x in expected)
print(plain)
```

### Python Source And Bytecode

If `.py` is provided:

- read constants and comparison functions
- decode Base64/hex before executing unknown logic
- remove sleeps and failure exits in a local copy
- use `dis` when the check is hidden in bytecode-style logic

```python
import dis

def check(value):
    return value[::-1] == "terces"

dis.dis(check)
```

### Java, APK, And WebAssembly

Java/APK:

```bash
jadx-gui app.apk
```

Check `MainActivity`, resources, hardcoded strings, native library loading, and validation methods.

WebAssembly:

```bash
wasm2wat module.wasm -o module.wat
wasm-decompile module.wasm > module.c
strings -n 8 module.wasm
```

Search for exported check functions, memory offsets, expected byte arrays, and simple transforms.

### Packed Or Obfuscated Binaries

```bash
upx -d ./challenge
file ./challenge
strings -n 8 ./challenge
```

If unpacking fails, debug runtime behavior and search for decrypted strings after the program initializes.

## Useful External References

- Anti-debug reference: https://anti-debug.checkpoint.com/
- PyLingual: https://www.pylingual.io/
- Online x86 assembler: https://defuse.ca/online-x86-assembler.htm
- pyinstxtractor: https://github.com/extremecoders-re/pyinstxtractor
- decompyle builds: https://github.com/extremecoders-re/decompyle-builds
- Local x86 guide: [Guide to x86 Assembly](../references/Guide%20to%20x86%20Assembly.html)
- Local syscall table: [Linux x86_64 syscall table](../references/Linux%20System%20Call%20Table%20for%20x86%2064%20-%20Ryan%20A.%20Chapman.html)
