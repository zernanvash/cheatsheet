# Crackme.exe writeup

Challenge_URL: https://crackmes.one/crackme/6a1e809417539b5175d12423

## summary

the correct key is:

```text
V1RTU4L_M4CH1N3_5T4CK
```

this was solved without patching the binary. the key was recovered by statically analyzing how `Crackme.exe` reads and decodes the three data files in `j/`, `d/`, and `k/`, then verified by running the program normally and entering the recovered key.

## target files

workspace:

```text
C:\Users\Princess Sallian\Downloads\Challenge
```

files:

```text
Crackme.exe   164352 bytes
README.md        262 bytes
j\d1.bin        2048 bytes
d\d2.bin        4096 bytes
k\d3.bin        3072 bytes
```

hashes:

```text
Crackme.exe
md5:    3bcff5815985d9d9848e2f122f87fbc9
sha1:   aecd370e7519da2cdab4071bf057c63530306843
sha256: 80841afe099a864e83e05c0169de0e720561f0c0a013e8aaf63e9cf8659b27be

j\d1.bin
sha256: cabd4f72ba76977f4f07a16eaee100b6bf0a68861ae615c73fa556f455d518d4

d\d2.bin
sha256: 412fd20de7f93694e83260eca302f5cdb508848d4472bfe408dcc0e55d390ef6

k\d3.bin
sha256: c3771b070f38bee158dffa4bb2fba0ec3abd28e84d2f644d129782f8086a3282
```

## tools used

all tool execution was done through rebridge mcp.

```text
die          initial compiler/file identification
radare2      imports, strings, disassembly, function flow
ghidra       headless import/analysis confirmation
capa         capability scan
python       small helper scripts for byte inspection and decode reproduction
```

## first observations

the readme gives the important hint:

```text
start by examining the j/, d/, and k/ directories.
not all data is what it seems.
think about what connects three separate files into one meaningful result.
```

that suggests the three `.bin` files are not random extras. byte inspection showed all three have high entropy and no obvious plaintext strings:

```text
j\d1.bin size 2048 entropy about 7.91
d\d2.bin size 4096 entropy about 7.96
k\d3.bin size 3072 entropy about 7.94
```

so the likely path was: the executable reads these files, decodes them, then compares the result to user input.

## binary triage

detect it easy identified the executable as a 64-bit windows pe built with visual studio/msvc:

```text
file type: PE64
compiler: Microsoft Visual C/C++ 19.36
linker:   Microsoft Linker 14.36
tool:     Visual Studio 2022
subsystem: console
```

important imports included:

```text
GetModuleFileNameA
CreateFileW
ReadFile
GetFileSizeEx
ReadConsoleW
WriteFile
IsDebuggerPresent
GetThreadContext
QueryPerformanceCounter
QueryPerformanceFrequency
GetProcAddress
LoadLibraryA
```

the import list already suggests both file-reading behavior and anti-debug behavior.

## useful strings

plain string extraction found the user-facing flow and the embedded paths:

```text
Access denied.
Loading verification data...
%sj\d1.bin
%sd\d2.bin
%sk\d3.bin
Error: Cannot load j/d1.bin
Error: Cannot load d/d2.bin
Error: Cannot load k/d3.bin
Decoding verification layers...
Error: Decode failed.
Error: Integrity check failed.
Initializing anti-debug protections...
Enter key:
Error reading input.
Empty key.
Validating...
*** ACCESS GRANTED ***
Key verified successfully.
*** ACCESS DENIED ***
Invalid key.
CheckRemoteDebuggerPresent
IsDebuggerPresent
```

this confirmed that the three side files are part of the intended verification data.

## main function overview

radare2 identified `main` at:

```text
0x140001010
```

the important behavior in `main` is:

1. initialize anti-debug-related state.
2. get the executable path with `GetModuleFileNameA`.
3. truncate the executable filename to keep the directory path.
4. build these three paths:

```text
<exe directory>\j\d1.bin
<exe directory>\d\d2.bin
<exe directory>\k\d3.bin
```

5. load all three files.
6. decode the verification layers.
7. check decoded data integrity.
8. read the user's key from the console.
9. compare the user input with the decoded expected key.
10. print either access granted or access denied.

the final comparison is straightforward. after decoding, the program compares the entered key byte-for-byte against an expected buffer. it also checks that the input length matches the expected length.

## file loading structure

the program stores each loaded file in a small structure. the three structures are placed 0x28 bytes apart in the main context:

```text
context + 0x00  -> first file, j\d1.bin
context + 0x28  -> second file, d\d2.bin
context + 0x50  -> third file, k\d3.bin
```

the file loading helper reads the whole file into memory and stores the raw pointer and size. a later helper allocates a second buffer and copies the data before decoding it.

## layer decode function

the most important function is:

```text
0x140001b90
```

this function is called three times by:

```text
0x140001b20
```

with layer indexes 0, 1, and 2.

at `0x140001b90`, the function selects one 8-byte constant from a table at:

```text
0x14001b848
```

the constants are:

```text
index 0: 0x564d3558aabbccdd
index 1: 0xabcd1234deadbeef
index 2: 0x9988776655443322
```

the raw table bytes are little-endian:

```text
dd cc bb aa 58 35 4d 56
ef be ad de 34 12 cd ab
22 33 44 55 66 77 88 99
```

for every byte in the layer, the decode function does this:

```text
decoded_byte = raw_byte
decoded_byte ^= key[(i - 4) & 7]
decoded_byte = ror8(decoded_byte, 3)
decoded_byte ^= key[i & 7]
```

where `key` is the selected 8-byte constant in little-endian byte order.

the rotate is an 8-bit rotate right by 3.

## reproducing the decode

this python script reproduces the important part of the binary logic:

```python
from pathlib import Path

root = Path(r"C:\Users\Princess Sallian\Downloads\Challenge")

files = [
    root / "j" / "d1.bin",
    root / "d" / "d2.bin",
    root / "k" / "d3.bin",
]

constants = [
    0x564d3558aabbccdd,
    0xabcd1234deadbeef,
    0x9988776655443322,
]

def ror8(x, n):
    return ((x >> n) | ((x << (8 - n)) & 0xff)) & 0xff

parts = []

for path, constant in zip(files, constants):
    key = constant.to_bytes(8, "little")
    raw = path.read_bytes()
    decoded = bytearray()

    for i, b in enumerate(raw):
        v = b ^ key[(i - 4) & 7]
        v = ror8(v, 3)
        v ^= key[i & 7]
        decoded.append(v)

    length = int.from_bytes(decoded[:2], "little")
    part = bytes(decoded[2:2 + length])
    parts.append(part)

    print(path, length, part)

print(b"".join(parts).decode("ascii"))
```

output:

```text
C:\Users\Princess Sallian\Downloads\Challenge\j\d1.bin 8 b'V1RTU4L_'
C:\Users\Princess Sallian\Downloads\Challenge\d\d2.bin 8 b'M4CH1N3_'
C:\Users\Princess Sallian\Downloads\Challenge\k\d3.bin 5 b'5T4CK'
V1RTU4L_M4CH1N3_5T4CK
```

## why those bytes are the key

after decoding, another function combines the decoded layer payloads.

each decoded file begins with a two-byte little-endian length. the bytes after that length are the actual useful fragment.

the decoded fragments are:

```text
j\d1.bin -> V1RTU4L_
d\d2.bin -> M4CH1N3_
k\d3.bin -> 5T4CK
```

joining them in the same order the program uses gives:

```text
V1RTU4L_M4CH1N3_5T4CK
```

in `main`, the program then reads console input, strips trailing whitespace, and compares it against this decoded buffer. if the length and all bytes match, it prints the granted message.

## verification

running the program normally with the recovered key:

```text
input:
V1RTU4L_M4CH1N3_5T4CK
```

produced:

```text
Loading verification data...
Decoding verification layers...
Initializing anti-debug protections...

Enter key: Validating...

*** ACCESS GRANTED ***
Key verified successfully.
```

this confirms the key is valid.

## anti-debug notes

the binary contains anti-debug checks, including:

```text
IsDebuggerPresent
CheckRemoteDebuggerPresent
NtQueryInformationProcess
NtSetInformationThread
GetThreadContext
QueryPerformanceCounter
QueryPerformanceFrequency
```

the solve did not require bypassing them. the key was recovered statically from the decode logic and verified by running the program without attaching a debugger.

## capa notes

capa confirmed the file as a windows amd64 pe and identified file-system and anti-analysis/tool-string related capabilities. the result was noisy because many runtime/library routines are present, but it supported the static observations:

```text
reads files
gets file size
references analysis/debugging related strings
uses environment/file APIs through the linked runtime
```

## final answer

```text
V1RTU4L_M4CH1N3_5T4CK
```

no binary patching was used.
