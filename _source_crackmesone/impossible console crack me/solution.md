# crackmeh.exe — Writeup

Challenge_URL: https://crackmes.one/crackme/69a1280d0b6d36e727710a97

**Analyst:** RootRevenant
**Date:** 2026-02-27
**Category:** Reverse Engineering / Unpacking
**Difficulty:** Easy
**Tools:** Binary Ninja, Python 3.12

---

## Overview

`crackmeh.exe` is a Windows PE32+ binary that acts as a custom packer. It
contains an encrypted crackme embedded in the PE overlay. The goal is to
unpack the inner binary and find the password. I solved this entirely through
static analysis on Linux — the binary was never executed.

| Property    | Value |
|-------------|-------|
| **File**    | crackmeh.exe |
| **Size**    | 69 347 bytes |
| **SHA-256** | `f297fc9117350e1242c61c66c42b64903bea4a60f0832565c6e8a6dba8380490` |
| **Arch**    | PE32+ (x86-64) |

---

## Step 1 — Initial Triage

I loaded the binary in Binary Ninja and started by examining the PE structure.
The outer binary has 6 standard sections (`.text`, `.rdata`, `.data`,
`.pdata`, `.rsrc`, `.reloc`) with the last section (`.reloc`) ending at file
offset `0xC400` (50 176 bytes). However, the total file size is 69 347 bytes.

This immediately tells us there are **19 171 bytes of overlay data** appended
after the PE sections — a classic indicator of a packer or self-extracting
archive. The outer binary's code likely reads this overlay at runtime,
decrypts it, and executes the result.

---

## Step 2 — Discovering the Trailer

Rather than diving into the packer's code first, I looked at the end of the
file in a hex editor. The last 60 bytes jumped out immediately:

```
Offset  Hex                                               ASCII
------  ------------------------------------------------  ----------------
0000    de c0 ad de 00 48 00 00 80 04 00 00 a7 02 00 00   .....H..........
0010    eb 60 11 49 40 b9 e5 72 f0 e9 e1 fc f7 1f 00 ab   .`.I@..r........
0020    90 09 0e c4 cb 8d 4e 27 a8 90 bc 89 c0 aa 4d d5   ......N'......M.
0030    de 15 eb 83 0f 2d 70 9c ef be ad de               .....-p.....
```

Two magic values are unmistakable:
- **`0xDEADC0DE`** at the start (bytes `de c0 ad de` in little-endian)
- **`0xDEADBEEF`** at the end (bytes `ef be ad de` in little-endian)

These sentinel markers frame a structured trailer. I mapped the fields by
cross-referencing with the packer's decompiled code in Binary Ninja:

| Offset | Size | Value        | Meaning                  |
|--------|------|--------------|--------------------------|
| 0x00   | 4    | `DEADC0DE`   | Magic start marker       |
| 0x04   | 4    | `0x4800`     | Inner PE size (18 432 B) |
| 0x08   | 4    | `0x0480`     | Additional metadata      |
| 0x0C   | 4    | `0x02A7`     | Additional metadata      |
| 0x10   | 16   | *(key data)* | XOR encryption key       |
| 0x20   | 24   | *(data)*     | Encrypted metadata block |
| 0x38   | 4    | `DEADBEEF`   | Magic end marker         |

The 16-byte XOR key extracted from offset 0x10:

```
eb 60 11 49 40 b9 e5 72 f0 e9 e1 fc f7 1f 00 ab
```

---

## Step 3 — Reversing the Encryption Algorithm

With the key in hand, I needed to understand how the packer encrypts the
payload. I analyzed the packer's decryption routine in Binary Ninja and found
a straightforward byte-level cipher:

**Encryption (what the packer does to produce the ciphertext):**
```
encrypted[i] = ROL8(plaintext[i] ^ key[i % 16], 3)
```

**Decryption (the inverse I need to apply):**
```
plaintext[i] = ROR8(encrypted[i], 3) ^ key[i % 16]
```

Where `ROL8` and `ROR8` are 8-bit bitwise rotate-left and rotate-right:
```python
def rol8(b, n):
    return ((b << n) | (b >> (8 - n))) & 0xFF

def ror8(b, n):
    return ((b >> n) | (b << (8 - n))) & 0xFF
```

The key is applied cyclically — each byte `i` of the plaintext is XORed with
`key[i % 16]`, then the result is rotated left by 3 bits. To reverse this,
I rotate right by 3, then XOR with the same key byte.

**My thought process:** The combination of XOR + rotation is slightly more
sophisticated than plain XOR, but still trivially reversible once you
identify the operations and their order. The rotation bits (3) were visible
as a constant in the decompiled loop.

---

## Step 4 — Decryption and Verification

The encrypted payload starts at file offset `0xC400` (right after the PE
sections) and the trailer tells us the inner PE is `0x4800` (18 432) bytes.
I wrote a Python decryptor and immediately verified the output:

```python
def decrypt(enc_data, key):
    result = bytearray(len(enc_data))
    for i, b in enumerate(enc_data):
        result[i] = ror8(b, 3) ^ key[i % 16]
    return bytes(result)
```

Decrypting the first 16 bytes produced:
```
4d 5a 90 00 03 00 00 00 04 00 00 00 ff ff 00 00
 M  Z
```

The `MZ` DOS signature confirmed the decryption was correct. I further
validated the output by checking:

- **PE signature** at the `e_lfanew` offset (0xF0) → `PE\x00\x00` ✓
- **Rich header** marker present in the first 1024 bytes ✓
- **Machine type** 0x8664 (AMD64) ✓
- **PE magic** 0x20B (PE32+) ✓

The decrypted binary is a valid PE32+ executable compiled with MSVC, as
indicated by the Rich header and PDB path:
```
C:\Users\kanax\source\repos\CrackMeEasy\x64\Release\CrackMeEasy.pdb
```

---

## Step 5 — Analyzing the Inner Crackme

The decrypted `CrackMeEasy.exe` (18 432 bytes, SHA-256:
`afca12717fb5a1294b84215fbecdac2020d7e350cf0a7f75a356a61ce632799d`)
has the following section layout:

| Section  | VA     | VSize   | Raw Offset | Raw Size |
|----------|--------|---------|------------|----------|
| `.text`  | 0x1000 | 0x1A93  | 0x0400     | 0x1C00   |
| `.rdata` | 0x3000 | 0x1D1C  | 0x2000     | 0x1E00   |
| `.data`  | 0x5000 | 0x0248  | 0x3E00     | 0x0200   |
| `.pdata` | 0x6000 | 0x0294  | 0x4000     | 0x0400   |
| `.rsrc`  | 0x7000 | 0x01E0  | 0x4400     | 0x0200   |
| `.reloc` | 0x8000 | 0x0060  | 0x4600     | 0x0200   |

Running a string search on the `.rdata` section revealed the crackme's UI
messages:

| Offset | String |
|--------|--------|
| 0x23C8 | `Welcome!!!` |
| 0x23D8 | `Please Enter The Password:` |
| 0x23FA | `Congrats!!! You Cracked The Code` |
| 0x2422 | `Wrong Password, Please Try Again` |

This tells us the crackme is a simple "enter the password" challenge using
`std::cin` / `std::cout`.

---

## Step 6 — Finding the Password

With the string references identified, I searched the `.data` section for
the password. The `.data` section starts at file offset `0x3E00` and is
`0x200` bytes. At offset `0xB8` within that section (file offset `0x3EB8`,
VA `0x1400050B8`), I found a plaintext null-terminated ASCII string:

```
EasyPassword
```

The crackme's main function reads input via `std::cin`, compares it against
this hardcoded string, and branches to either the success message
("Congrats!!! You Cracked The Code") or the failure message ("Wrong Password,
Please Try Again").

**My thought process:** Given the crackme's name ("CrackMeEasy") and the
plaintext storage in `.data`, the author clearly intended this as a
beginner-level challenge. No hashing, no obfuscation — just a direct string
comparison. The real challenge was the packer layer wrapping it.

---

## Solution

| Component            | Answer                             |
|----------------------|------------------------------------|
| **Packer XOR key**   | `eb60114940b9e572f0e9e1fcf71f00ab` |
| **Crypto algorithm** | `ROL8(byte ^ key[i%16], 3)`        |
| **Inner crackme**    | CrackMeEasy.exe (18 432 bytes)     |
| **Password**         | **`EasyPassword`**                 |

---

## Automated Solver

I wrote a Python solver (`crackmeh_solver.py`) that automates the complete
unpacking and password extraction pipeline:

```
$ python crackmeh_solver.py crackmeh.exe
XOR key:    eb60114940b9e572f0e9e1fcf71f00ab
Algorithm:  ROL8(byte ^ key[i%16], 3)
Inner PE:   CrackMeEasy.exe (18432 bytes)
Password:   EasyPassword
Saved:      CrackMeEasy.exe
```

The solver:
1. Reads the 60-byte trailer and extracts the XOR key
2. Reads the encrypted payload from the PE overlay
3. Decrypts using `ROR8(byte, 3) ^ key[i % 16]`
4. Validates the decrypted PE (MZ + PE signatures)
5. Searches the `.data` section for the password
6. Writes the decrypted `CrackMeEasy.exe` to disk

The solver includes a comprehensive test suite (21 tests) covering
bit rotation primitives, key extraction, decryption correctness, PE header
validation, password extraction, and output file generation.

---

## Artifacts Included

| File                      | Description                                                                                          |
|---------------------------|------------------------------------------------------------------------------------------------------|
| `crackmeh_solver.py`      | Standalone solver — parses the trailer, extracts the XOR key, decrypts the inner PE, and prints the password. Run with `python crackmeh_solver.py crackmeh.exe`. |
| `test_crackmeh_solver.py` | pytest test suite (21 tests) validating every step: bit rotation primitives, key extraction, decryption correctness, PE header integrity, and password recovery. |

---

*RootRevenant — 2026-02-27*
