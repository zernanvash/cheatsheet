# Temperance Challenge Solutions (levelx00-levelx32)

This page is the offline solution companion for the 33 HackMyVM HMVLabs Temperance scripts in `_source_temperance/`. It extracts the evidenced transformation from each source file, explains the relevant Python technique, and replaces fragile wildcard-import behavior with explicit, reusable code.

> The upstream service is historical and may be unavailable or may return different randomized inputs. The flags below are recorded results from the transcripts preserved in the local source files; they were not revalidated against the live service during this documentation pass.

## Navigation

- [Setup](#setup)
- [Reusable Service Client](#reusable-service-client)
- [Level Summary and Recorded Flags](#level-summary-and-recorded-flags)
- [Levels 00-08: Basic Bytes and Arithmetic](#levels-00-08-basic-bytes-and-arithmetic)
- [Levels 09-15: Text Decoding and Parsing](#levels-09-15-text-decoding-and-parsing)
- [Levels 16-23: Images, Archives, Hashes, and Binary Data](#levels-16-23-images-archives-hashes-and-binary-data)
- [Levels 24-29: HTTP, JWT, OCR, and Coordinates](#levels-24-29-http-jwt-ocr-and-coordinates)
- [Levels 30-32: XOR, QR, and Permutations](#levels-30-32-xor-qr-and-permutations)
- [Corrections to the Preserved Source](#corrections-to-the-preserved-source)

## Setup

The early levels require only Python and pwntools. Later levels add Pillow, Requests, PyJWT, geopy, Tesseract OCR, and zbar QR decoding.

```bash
python3 -m venv temperance-env
source temperance-env/bin/activate
python -m pip install --upgrade pip
python -m pip install pwntools pillow requests PyJWT geopy pytesseract pyzbar
sudo apt update
sudo apt install -y tesseract-ocr libzbar0
```

On Windows, activate the virtual environment with:

```powershell
py -m venv temperance-env
.\temperance-env\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install pwntools pillow requests PyJWT geopy pytesseract pyzbar
```

Tesseract and the zbar shared library must also be installed separately and available on `PATH` on Windows.

## Reusable Service Client

The preserved service protocol sends a banner, accepts a level name, sends one challenge value, and expects raw answer bytes. Most levels fit this runner:

```python
from collections.abc import Callable

from pwn import remote

HOST = "temperance.hackmyvm.eu"
PORT = 9988


def run_level(level_name: str, solve: Callable[[bytes], bytes | str]) -> None:
    with remote(HOST, PORT) as tube:
        print(tube.recv(timeout=2).decode(errors="replace"))
        tube.send(level_name.encode())

        challenge = tube.recv(65536, timeout=3)
        print(f"challenge={challenge!r}")

        answer = solve(challenge)
        if isinstance(answer, str):
            answer = answer.encode()
        tube.send(answer)

        print(tube.recv(4096, timeout=3).decode(errors="replace"))
```

Use `send()`, not `sendline()`, unless the service explicitly requests a newline. Network reads are stream-based rather than message-based; if the live service changes its framing, prefer `recvuntil()` or `recvline()` with an observed delimiter.

Level 01 is the exception because it performs two receive-and-echo rounds:

```python
from pwn import remote

with remote(HOST, PORT) as tube:
    tube.recv(timeout=2)
    tube.send(b"levelx01")
    for _ in range(2):
        challenge = tube.recv(4096, timeout=2)
        tube.send(challenge)
    print(tube.recv(4096, timeout=2).decode(errors="replace"))
```

## Level Summary and Recorded Flags

| Level | Required transformation | Core Python | Recorded flag |
| --- | --- | --- | --- |
| 00 | Echo one byte string | `data` | `HMV{hell0friendz}` |
| 01 | Echo two successive strings | two receive/send rounds | `HMV{3ch03zlol}` |
| 02 | Convert to uppercase | `data.upper()` | `HMV{uPP3rc4z3z}` |
| 03 | Decode Base64 | `base64.b64decode()` | `HMV{baz364WTF}` |
| 04 | Reverse the bytes | `data[::-1]` | `HMV{r3vr3vr3v}` |
| 05 | Return the final five bytes | `data[-5:]` | `HMV{l4ztf1v3wh0t}` |
| 06 | Return the byte length as text | `str(len(data))` | `HMV{idkl3ng7hzZz}` |
| 07 | Decode hexadecimal to bytes | `bytes.fromhex()` | `HMV{zup3rh3x4haha}` |
| 08 | Add two integers | `sum()` | `HMV{1l34rnzum}` |
| 09 | Decode ROT13 | `codecs.decode()` | `HMV{r0t13izmyfr1end}` |
| 10 | Sort numbers and concatenate | `sorted(map(int, ...))` | `HMV{1mthez0rt3r}` |
| 11 | Decode Morse code | inverse lookup table | `HMV{d0tz4ndashez}` |
| 12 | Repeat a string `n` times | `text * count` | `HMV{ztr1ngc0nc4444t3nat3}` |
| 13 | Return alphabetically last string | `max(words)` | `HMV{WTF1zthatl3vel}` |
| 14 | Count a selected character | `text.count(char)` | `HMV{f1ndthec0rrectch4r}` |
| 15 | Extend an arithmetic sequence | last value plus common difference | `HMV{s3qu3nz3123}` |
| 16 | Read PNG dimensions | `Image.size` | `HMV{p4int3rPNGfile}` |
| 17 | Read a one-pixel PNG alpha value | `getpixel((0, 0))[-1]` | `HMV{RGBAsteg0u}` |
| 18 | Convert every input byte to eight bits | `f"{byte:08b}"` | `HMV{0n3sandz3r0esuhm}` |
| 19 | Extract text from a Base64 ZIP | `zipfile.ZipFile` | `HMV{z1pandtxtar3h3r3}` |
| 20 | Match an MD5 against RockYou candidates | `hashlib.md5()` | `HMV{r0ckur0ckme}` |
| 21 | Convert bytes to KiB-style KB text | divide by 1024 and format | `HMV{k1l0b33tz}` |
| 22 | Convert decimal code points to ASCII | `chr(int(value))` | `HMV{4sc111sg00d}` |
| 23 | Decode text from PNG alpha channels | alpha value to `chr()` | `HMV{n00bzt3g0}` |
| 24 | Fetch and return an HTTP body | `requests.get().text` | `HMV{1nt3rn3tw0w}` |
| 25 | Return the `Hmv-Code` response header | `response.headers` | `HMV{h3ad3rc0ntr0l}` |
| 26 | OCR digits from a Base64 PNG | `pytesseract.image_to_string()` | `HMV{c4ptchm3numb3rz}` |
| 27 | Return the proxy user's UID | parse passwd-style fields | `HMV{pr0xykn0wur1d}` |
| 28 | Verify HS256 JWT and read `HMVKey` | `jwt.decode()` | `HMV{jWth4f4ck}` |
| 29 | Calculate geodesic distance | `geodesic().kilometers` | `HMV{wh3r314ml0st}` |
| 30 | Repeating-key XOR with `HMV` | byte-wise XOR | `HMV{x0rmex0ru}` |
| 31 | Decode a QR code from a Base64 PNG | `pyzbar.decode()` | `HMV{4rtQRc0d3z}` |
| 32 | Permute text until its MD5 matches | `itertools.permutations()` | `HMV{p3rmut4t10n0np3r}` |

## Levels 00-08: Basic Bytes and Arithmetic

These levels establish the bytes/text boundary used throughout pwntools. Keep data as bytes when a byte transform is sufficient; decode only for text parsing.

```python
import base64


def solve00(data: bytes) -> bytes:
    return data


def solve02(data: bytes) -> bytes:
    return data.upper()


def solve03(data: bytes) -> bytes:
    return base64.b64decode(data)


def solve04(data: bytes) -> bytes:
    return data[::-1]


def solve05(data: bytes) -> bytes:
    return data[-5:]


def solve06(data: bytes) -> str:
    return str(len(data))


def solve07(data: bytes) -> bytes:
    return bytes.fromhex(data.decode())


def solve08(data: bytes) -> str:
    return str(sum(map(int, data.split())))
```

Examples:

```python
assert solve02(b"wegomakeittrue") == b"WEGOMAKEITTRUE"
assert solve03(b"eW91bWFrZW1lY3J5") == b"youmakemecry"
assert solve04(b"crazy") == b"yzarc"
assert solve05(b"IDKWhyimdoingthisshit") == b"sshit"
assert solve07(b"484d56") == b"HMV"
assert solve08(b"45 77") == "122"
```

## Levels 09-15: Text Decoding and Parsing

### Level 09: ROT13

ROT13 is reciprocal: the same transform encrypts and decrypts.

```python
import codecs


def solve09(data: bytes) -> str:
    return codecs.decode(data.decode(), "rot_13")
```

### Level 10: Numeric Sort and Concatenation

Parse before sorting. Sorting decoded strings directly is lexicographic, which misorders values of different digit lengths.

```python
def solve10(data: bytes) -> str:
    numbers = sorted(map(int, data.split()))
    return "".join(map(str, numbers))


assert solve10(b"80 37 67 41 31") == "3137416780"
```

### Level 11: Morse Code

```python
MORSE_SYMBOLS = (
    ".- -... -.-. -.. . ..-. --. .... .. .--- -.- .-.. -- -. --- .--. "
    "--.- .-. ... - ..- ...- .-- -..- -.-- --.. ----- .---- ..--- ...-- "
    "....- ..... -.... --... ---.. ----."
).split()
MORSE_TO_TEXT = dict(zip(MORSE_SYMBOLS, "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"))


def solve11(data: bytes) -> str:
    return "".join(MORSE_TO_TEXT[token] for token in data.decode().split())
```

### Levels 12-15: Repetition, Selection, Counting, and Sequences

```python
def solve12(data: bytes) -> str:
    text, count = data.decode().split()
    return text * int(count)


def solve13(data: bytes) -> str:
    words = data.decode().strip().removeprefix("[").removesuffix("]").split()
    return max(words)


def solve14(data: bytes) -> str:
    text, character = data.decode().rsplit(" ", 1)
    return str(text.count(character))


def solve15(data: bytes) -> str:
    numbers = list(map(int, data.split()))
    difference = numbers[1] - numbers[0]
    return str(numbers[-1] + difference)
```

Level 15 assumes the evidenced arithmetic progression. For an unknown sequence challenge, verify every adjacent difference instead of extrapolating from only the first pair.

## Levels 16-23: Images, Archives, Hashes, and Binary Data

### Shared Image Loader

```python
import base64
import io

from PIL import Image


def image_from_base64(data: bytes) -> Image.Image:
    return Image.open(io.BytesIO(base64.b64decode(data)))
```

### Levels 16-18: PNG Metadata, Alpha, and Binary Text

```python
def solve16(data: bytes) -> str:
    image = image_from_base64(data)
    width, height = image.size
    return f"{width}x{height}"


def solve17(data: bytes) -> str:
    image = image_from_base64(data).convert("RGBA")
    return str(image.getpixel((0, 0))[3])


def solve18(data: bytes) -> str:
    return "".join(f"{byte:08b}" for byte in data)
```

The explicit `:08b` width in level 18 preserves leading zero bits for every byte. Converting the entire message to one integer can lose leading zeroes.

### Level 19: Base64 ZIP in Memory

```python
import zipfile


def solve19(data: bytes) -> bytes:
    archive_data = base64.b64decode(data)
    with zipfile.ZipFile(io.BytesIO(archive_data)) as archive:
        names = archive.namelist()
        if not names:
            raise ValueError("ZIP archive contains no files")
        return archive.read(names[0]).strip()
```

### Level 20: Small-Dictionary MD5 Lookup

The preserved candidate file is `_source_temperance/rockyou_top100`; only its first 50 lines are used by this level.

```python
import hashlib
from pathlib import Path


def solve20(data: bytes, wordlist: Path) -> str:
    target = data.decode().strip().lower()
    candidates = wordlist.read_text(encoding="utf-8").splitlines()[:50]
    for word in candidates:
        if hashlib.md5(word.encode()).hexdigest() == target:
            return word
    raise ValueError("MD5 was not found in the first 50 candidates")


answer = solve20(challenge, Path("_source_temperance/rockyou_top100"))
```

This is a bounded CTF lookup, not a recommendation to store real passwords with MD5.

### Levels 21-23: Formatting, ASCII, and Alpha-Channel Steganography

```python
def solve21(data: bytes) -> str:
    return f"{int(data) / 1024:.2f}KB"


def solve22(data: bytes) -> str:
    return "".join(chr(int(value)) for value in data.split())


def solve23(data: bytes) -> str:
    image = image_from_base64(data).convert("RGBA")
    return "".join(chr(image.getpixel((x, y))[3])
                   for x in range(image.width)
                   for y in range(image.height))
```

Level 21 calls the result `KB` but divides by 1024, which is binary KiB-style conversion. Match the challenge's expected label exactly.

## Levels 24-29: HTTP, JWT, OCR, and Coordinates

Treat challenge-provided URLs as untrusted outside the authorized lab. The functions below restrict the hostname to the recorded Temperance service before making a request.

```python
from urllib.parse import urlparse

import requests

ALLOWED_HOST = "temperance.hackmyvm.eu"


def get_challenge_url(data: bytes) -> requests.Response:
    url = data.decode().strip()
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or parsed.hostname != ALLOWED_HOST:
        raise ValueError("unexpected challenge URL")
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response
```

### Levels 24-25: HTTP Body and Header

```python
def solve24(data: bytes) -> str:
    return get_challenge_url(data).text


def solve25(data: bytes) -> str:
    return get_challenge_url(data).headers["Hmv-Code"]
```

The level 25 mission comment calls the header `HMV-Header`, but its example response and working source code use `Hmv-Code`. HTTP header names are case-insensitive; the actual name difference is not.

### Level 26: OCR

```python
import pytesseract


def solve26(data: bytes) -> str:
    image = image_from_base64(data)
    text = pytesseract.image_to_string(
        image,
        config="--psm 7 -c tessedit_char_whitelist=0123456789",
    )
    result = "".join(character for character in text if character.isdigit())
    if not result:
        raise ValueError("OCR did not find digits")
    return result
```

### Level 27: passwd-Style Parsing

```python
def solve27(data: bytes) -> str:
    for line in get_challenge_url(data).text.splitlines():
        fields = line.split(":")
        if len(fields) >= 3 and fields[0] == "proxy":
            return fields[2]
    raise ValueError("proxy user was not present")
```

### Level 28: JWT Verification

```python
import jwt


def solve28(data: bytes) -> str:
    claims = jwt.decode(data.decode(), "secret", algorithms=["HS256"])
    return claims["HMVKey"]
```

Specifying the expected algorithm prevents algorithm-confusion behavior. The key `secret` is challenge-provided/default lab knowledge and must not be generalized to real tokens.

### Level 29: Geodesic Distance

```python
import re

from geopy.distance import geodesic

COORDINATES = re.compile(
    r"Lat:\s*(-?\d+(?:\.\d+)?)\s+Lon:\s*(-?\d+(?:\.\d+)?)\s*-\s*"
    r"Lat:\s*(-?\d+(?:\.\d+)?)\s+Lon:\s*(-?\d+(?:\.\d+)?)"
)


def solve29(data: bytes) -> str:
    match = COORDINATES.fullmatch(data.decode().strip())
    if not match:
        raise ValueError("unexpected coordinate format")
    lat_a, lon_a, lat_b, lon_b = map(float, match.groups())
    distance = geodesic((lat_a, lon_a), (lat_b, lon_b)).kilometers
    return f"{distance:.3f}"
```

Formatting with `.3f` guarantees exactly three decimal places; `str(round(value, 3))` can omit trailing zeroes.

## Levels 30-32: XOR, QR, and Permutations

### Level 30: Repeating-Key XOR

```python
def solve30(data: bytes) -> bytes:
    key = b"HMV"
    return bytes(value ^ key[index % len(key)]
                 for index, value in enumerate(data))
```

XOR is reciprocal, so the same function encrypts and decrypts. Operating on bytes avoids encoding errors caused by control characters in the challenge value.

### Level 31: QR Decoding

```python
from pyzbar.pyzbar import decode as decode_barcodes


def solve31(data: bytes) -> str:
    image = image_from_base64(data)
    decoded = decode_barcodes(image)
    if not decoded:
        raise ValueError("no QR or barcode payload was detected")
    return "".join(item.data.decode("utf-8") for item in decoded)
```

### Level 32: MD5-Guided Permutation Search

```python
import hashlib
import itertools


def solve32(data: bytes) -> str:
    target, characters = data.decode().split()
    for candidate_tuple in itertools.permutations(characters):
        candidate = "".join(candidate_tuple)
        if hashlib.md5(candidate.encode()).hexdigest() == target:
            return candidate
    raise ValueError("no permutation matched the supplied MD5")
```

This costs `n!` hashes and is practical only because the evidenced strings are short. Repeated characters cause duplicate permutations; deduplication can save work, but storing every permutation also consumes memory. For a larger input, derive more constraints before brute force.

## Corrections to the Preserved Source

The `_source_temperance` directory remains unchanged. This companion makes the following corrections explicitly:

| Level | Preserved behavior | Companion behavior |
| --- | --- | --- |
| 10 | Sorts decoded number strings lexicographically | Parses integers before sorting |
| 18 | Reaches `binascii` through `from pwn import *` and converts the entire message as one integer | Formats each byte with `:08b`, preserving leading zeroes |
| 19 | Keeps only the last line read from the first ZIP member | Reads the first member directly and validates that it exists |
| 25 | Mission says `HMV-Header`; response and code say `Hmv-Code` | Uses the evidenced `Hmv-Code` header |
| 26 | Sends raw Tesseract output, potentially including whitespace | Whitelists digits and removes OCR whitespace/noise |
| 27 | Matches any line containing `proxy` | Requires the username field to equal `proxy` |
| 29 | Extracts only unsigned integer coordinates and uses `round()` | Accepts signed decimals and emits exactly three decimal places |
| 30 | Decodes arbitrary XOR input as text | XORs raw bytes |
| 31 | Uses `base64` without importing it explicitly | Imports all dependencies explicitly through shared helpers |

## Source Map

- Raw preserved scripts: `_source_temperance/levelx00.py` through `_source_temperance/levelx32.py`
- Candidate list for level 20: `_source_temperance/rockyou_top100`
- Generalized helper reference: [REV Python Toolkit](../tools/REV%20Python%20Toolkit.md)
- Source tracking: [Source Inventory](../references/Source%20Inventory.md)

> 💡 **What to watch out for:** The recorded scripts use `recv(1024)` and wildcard imports for brevity. For new challenges, use explicit imports, inspect protocol delimiters, preserve bytes until text decoding is required, and validate output formatting exactly.
