# CTF Primer Foundations

Use this page before category-specific blueprints when the challenge is unfamiliar and you need a reliable first-pass workflow. It adapts core lessons from the official [picoCTF CTF Primer](https://primer.picoctf.org/) into this vault's command and evidence conventions.

## The Universal Challenge Loop

```text
preserve -> identify -> inspect -> form a hypothesis -> test one variable -> record -> pivot
```

1. Preserve the original artifact and calculate a hash.
2. Identify the real file type instead of trusting its extension.
3. Collect cheap metadata, strings, and structure before using specialized tools.
4. State what you think is happening and what evidence would confirm it.
5. Change one input or assumption at a time.
6. Save commands, outputs, offsets, and decoded intermediates.
7. If evidence contradicts the hypothesis, return to identification instead of forcing a tool.

```bash
sha256sum ./challenge
file ./challenge
stat ./challenge
strings -a -n 6 ./challenge | head -n 80
```

> 💡 **What to watch out for:** A filename is a hint, not evidence. ZIP data may be renamed, a PNG may contain trailing data, and a text file may contain encoded bytes.

## Shell Literacy for CTF Work

A shell command is normally:

```text
program [options] [arguments]
```

Learn a new tool by checking its built-in help before copying an unknown command:

```bash
tool --help
man tool
apropos keyword
type tool
which tool
```

Square brackets in usage text usually mark optional arguments; unbracketed operands are normally required. Exit a man page with `q`. Use Tab completion to reduce path mistakes and the up arrow or `history` to reuse commands.

### Pipes and redirection

```bash
file ./challenge
strings -a ./challenge | grep -Ei 'flag|pass|key'
find . -type f -print0 | xargs -0 file
command > output.txt
command 2> errors.txt
command | tee evidence.txt
```

- `|` sends one program's standard output to another program.
- `>` replaces a file with output; `>>` appends.
- `2>` captures standard error.
- Quote paths and patterns when spaces or shell metacharacters are possible.

## Searching Files and Content

Separate two questions: “Which file?” and “Which content?”

```bash
find . -type f -iname '*secret*'
find . -type f -size +1M
grep -RniE 'flag\{|picoCTF\{|password|token' .
rg -n -i 'flag\{|password|token' .
```

For opaque or binary artifacts:

```bash
strings -a ./artifact | grep -Ei 'flag|password|key'
xxd -g 1 -l 256 ./artifact
binwalk ./artifact
```

## Forensics: Artifact Before Tool

Start with the container and work inward:

```text
download/archive -> extracted file -> partition -> filesystem -> inode/file -> content
```

```bash
file ./artifact
exiftool ./artifact
7z l ./artifact
binwalk ./artifact
```

Do not mount or modify the only copy. Work from a duplicate and record its hash.

### Disk-image reasoning

First determine whether the image contains a partition table:

```bash
mmls ./disk.img
fdisk -l ./disk.img
```

The Sleuth Kit commonly expects an offset in sectors, not bytes:

```bash
fls -r -p -o START_SECTOR ./disk.img
icat -o START_SECTOR ./disk.img INODE > recovered.bin
```

Replace `START_SECTOR` and `INODE` with values obtained from the image. Use `fls -d` to focus on deleted entries when relevant. Keep extraction output separate from the evidence image.

### Packet reasoning

For each packet or stream ask:

- Which endpoints and ports are communicating?
- Which protocol is actually present?
- Is the payload plaintext, encoded, compressed, or encrypted?
- Does reassembling a stream reveal a file, command, credential, or flag?

```bash
tshark -r ./capture.pcapng -q -z io,phs
tshark -r ./capture.pcapng -q -z conv,tcp
tshark -r ./capture.pcapng -Y 'http.request'
tshark -r ./capture.pcapng -Y 'dns.qry.name' -T fields -e dns.qry.name
```

## Python as CTF Glue

Use Python to make transformations repeatable, not as a substitute for understanding the data type.

```python
#!/usr/bin/env python3
from pathlib import Path

data = Path("challenge.bin").read_bytes()
print(f"length={len(data)}")
print(data[:32].hex())
```

### Text, bytes, and integers

```python
from pwn import p32, p64, u32, u64

text = "flag"
raw = text.encode()
restored = raw.decode()

little_32 = p32(0x41424344)
little_64 = p64(0x4142434445464748)
value_32 = u32(little_32)
value_64 = u64(little_64)
```

- `str` represents text.
- `bytes` represents raw octets used by files, sockets, and exploits.
- Packing converts integers to an architecture-sized byte representation.
- Endianness determines byte order; confirm it from the target architecture.

### Robust challenge scripts

```python
#!/usr/bin/env python3
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("artifact", type=Path)
args = parser.parse_args()

try:
    data = args.artifact.read_bytes()
except OSError as error:
    raise SystemExit(f"could not read artifact: {error}")

print(data[:64].hex())
```

Keep parsing, transformation, and validation separate. Test decoded output for expected length, magic bytes, printable structure, or a known format instead of accepting anything that “looks readable.”

## Web: Follow the Data Across Boundaries

A browser view is only one representation of the application. Track data through:

```text
URL -> HTTP request -> route -> server logic -> database/interpreter -> response -> browser DOM
```

For a normal request, record method, path, query, headers, cookies, body, status, redirect, response length, and visible result. Then change one field at a time.

```bash
curl -i "$URL/"
curl -i -X POST "$URL/login" \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  --data 'username=test&password=test'
```

Client-side validation is not authorization. JavaScript, hidden inputs, and disabled buttons can explain intended behavior, but the server must independently enforce trust decisions.

## Cryptography: Classify Before Decoding

Ask which operation family best explains the artifact:

| Family | Recognition question |
|---|---|
| Encoding | Can it be reversed without a secret key? |
| Substitution | Are symbols replaced while position is mostly preserved? |
| Transposition | Are symbols preserved but reordered? |
| Keyed classical cipher | Does a repeating or position-dependent key alter symbols? |
| Hash | Is it fixed-length and intended to be one-way? |
| Modern encryption | Are a key, nonce/IV, mode, tag, or block constraints present? |

Do not equate Base64, hexadecimal, compression, hashing, and encryption. Decode in layers and save every intermediate result.

## C Memory Model for PWN and REV

C arrays occupy contiguous memory and do not automatically enforce bounds at runtime. An expression such as `array[index]` computes an address from a base pointer, index, and element size. An invalid index can therefore access adjacent memory.

```c
int values[5];
int *pointer = values;
```

Conceptually:

```text
&values[index] == base_address + index * sizeof(int)
```

That relationship connects C source to disassembly:

- local arrays often become stack-frame offsets
- pointer dereferences become memory operands
- comparisons become conditional branches
- function calls save a return location
- an unchecked copy into a local array may overwrite adjacent control data

Compile a small lab program both with and without debug information and compare source, assembly, and runtime state:

```bash
gcc -g -O0 ./example.c -o ./example
objdump -d -M intel ./example
gdb -q ./example
```

Do not disable mitigations outside intentionally vulnerable local exercises.

## Assembly Reading Loop

Do not read assembly as isolated instructions. Read small blocks:

1. Identify function entry and stack-frame setup.
2. Track where input values enter registers or memory.
3. Find comparisons and the flags they set.
4. Follow conditional branches to success and failure paths.
5. Identify calls and apply the architecture's calling convention.
6. Confirm the hypothesis dynamically.

```gdb
set disassembly-flavor intel
disassemble main
break main
run
info registers
x/16gx $rsp
```

AT&T and Intel are two syntaxes for the same machine instructions; they are not different CPU architectures.

## Regex for Flag and Signal Extraction

Regex is useful when you know the shape but not the exact value.

```bash
rg -n 'picoCTF\{[^}]+\}' .
rg -n -i '\b(flag|secret|token|password)\b' .
```

```python
import re

matches = re.findall(rb"picoCTF\{[^}]+\}", data)
for match in matches:
    print(match.decode(errors="replace"))
```

Use narrow patterns first. A broad expression over large binary or minified data creates noise and may hide the useful match.

## Where to Continue

- Shell, ports, and services: [Networking And Linux Fundamentals](Networking%20And%20Linux%20Fundamentals.md)
- Forensic artifacts: [Forensics and Blue Team Playbook](../guides/Forensics%20and%20Blue%20Team%20Playbook.md)
- HTTP and browser behavior: [Web Fundamentals](Web%20Fundamentals.md)
- C, assembly, and binaries: [Reverse Engineering Fundamentals](Reverse%20Engineering%20Fundamentals.md)
- Stack corruption: [Ret2win Guide](../guides/Ret2win%20Guide.md)
- Encodings and ciphers: [Steganography And Cryptography Fundamentals](Steganography%20And%20Cryptography%20Fundamentals.md)
- Python helpers: [REV Python Toolkit](../tools/REV%20Python%20Toolkit.md)
- Operational workflows: [Blueprint Index](../blueprints/Blueprint%20Index.md)

## Source

This learning page is an original vault-oriented adaptation of concepts taught by Samuel Sabogal Pardo, Jeffery John, and Luke Jones in the official [picoCTF CTF Primer](https://primer.picoctf.org/). Examples use this vault's variable conventions and do not reproduce challenge flags or walkthrough answers.
