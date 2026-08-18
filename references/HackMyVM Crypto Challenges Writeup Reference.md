# HackMyVM Crypto Challenges Writeup Reference

Independent English study notes for 26 HackMyVM crypto challenges covered by the Chinese article [hackmyvm_challenge_crypto专题](https://blog.csdn.net/f1agccc/article/details/147709479). This is a technique-focused translation and analysis, not a mirror of the article. Large payloads and screenshots are intentionally omitted.

> **Source and verification:** The source article was published on 2025-05-05 and is marked CC BY-SA 4.0. Short text transformations were checked where the article supplied enough input. Results that depend on an original image, archive, or interactive visual step are labeled **artifact-dependent** and remain source-reported rather than independently verified. The current [HackMyVM challenges page](https://hackmyvm.eu/challenges/) requires authentication, so challenge artifacts were not fetched from it.

## Contents

- [Fast technique map](#fast-technique-map)
- [Challenge writeups](#challenge-writeups)
- [Reusable offline helpers](#reusable-offline-helpers)
- [Analysis and corrections](#analysis-and-corrections)
- [Related vault pages](#related-vault-pages)
- [Attribution](#attribution)

## Evidence labels

- **Text-checkable** — the article exposes a short input and a standard transformation that can be reproduced locally.
- **Intermediate-backed** — the article exposes meaningful intermediate values, but the complete original artifact or one decoding stage is unavailable.
- **Artifact-dependent** — the result relies on an image, archive, barcode, visual puzzle, or external decoder and is recorded as reported by the source.

## Fast technique map

| Challenge | Main recognition clue | Decode chain | Reported result | Evidence |
|---|---|---|---|---|
| 001 | Base64 alphabet and padding | Base64 → text | `hmv{base64decoder}` | Text-checkable |
| 004 | Even-length hexadecimal | Hex bytes → ASCII | `hmv{myflagiseasy}` | Text-checkable |
| 007 | Upside-down/mirrored Unicode | Normalize orientation → Base64 | `HMV{4v1jN3y4m}` | Text-checkable after normalization |
| 010 | Printable Base85-like text | Ascii85/Base85 → text | `HMV{wrtzxcvfdghyt}` | Text-checkable |
| 013 | Repeated-key classical cipher | Vigenère with key `FLAG` | `HMV{VIGNERECYPHER}` | Text-checkable |
| 017 | Six-dot cells | Braille → text | `hmv{idontknowbraille}` | Artifact-dependent |
| 023 | Cisco Type 7 marker/hex | Cisco Type 7 → text | `HMV{myciscoflag}` | Text-checkable |
| 035 | Known plaintext and custom alphabet | Recover Vigenère key → decrypt | `HMV{h0w_d0_y0u_g37_th15}` | Intermediate-backed |
| 044 | Address begins with `bc1q` | Identify Bitcoin native SegWit address | `HMV{Bech32}` | Text-checkable identification |
| 046 | `x`/`y` fragments and nested text | Join → Base64 → substitution → Base64 | `HMV{recursion}` | Intermediate-backed |
| 049 | Base64 that decodes to a PNG | Base64 → image → Pigpen | `HMV{notilluminati}` | Artifact-dependent |
| 051 | Restricted alphanumeric ciphertext | Twin Hex decoder | `HMV{4noth3r_C1pher}` | Intermediate-backed |
| 056 | Large Unicode symbol alphabet | Base2048 → text | `HMV{Base2048}` | Artifact-dependent |
| 057 | Large Unicode symbol alphabet | Base65536 → text | `HMV{where_have_you_been_rpj7_:)}` | Artifact-dependent |
| 058 | D'ni numeral glyphs | Glyphs → base-25 digits → integer | `HMV{13377331}` | Intermediate-backed |
| 061 | Base64 plus archive signature | Base64 → ZIP → binary → ternary → ASCII | `HMV{RPJ7_1_H0P3_Y0U_Cr4CK3D_17}` | Intermediate-backed |
| 062 | Barcode image | Code 128 scan | `HMV{1_l0v3_c0d3_128}` | Artifact-dependent |
| 066 | Chinese numerals and accented pinyin | Symbols → hex → text → Rail Fence (7) | `HMV{Special_greetings_to_my_dear_Chinese_friends}` | Intermediate-backed |
| 068 | Visually similar Unicode characters | Homoglyph/Unicode steganography | `hmvgreetings_from_green_br0ther` | Artifact-dependent; source omits braces |
| 069 | Raw bytes plus `HM@....@` hint | Known-format nibble substitution | `HM@HACK@` | Intermediate-backed |
| 071 | Long prose resembling a public article | Known-plaintext substitution | `HMV{is_the_best_website_for_vulnerable_virtual_machines}` | Intermediate-backed |
| 080 | Anchored regex and backreferences | Construct a matching string | `HMV{Regex_4_the_Win}` | Text-checkable with caveat |
| 081 | File contains only space, tab, newline | Binary regions + Morse region | Long plaintext answer below | Intermediate-backed |
| 082 | Mixed-width Unicode byte patterns | Segment UTF-8/UTF-16/UTF-32 | `HMV{power_of_UTF}` | Intermediate-backed |
| 087 | Encoded data produces cube moves | Base64 → repeating-key XOR → Rubik's Cube | `flag{T}` | Artifact-dependent |
| 089 | Layered printable encodings | Base64 → hex → reverse | `FLAG{D3c1ph3r1ng_1s_fun}` | Text-checkable |

## Challenge writeups

### 001 — Base64

The trailing padding and restricted alphabet suggest Base64. Decoding `aG12e2Jhc2U2NGRlY29kZXJ9` directly produces `hmv{base64decoder}`.

**Lesson:** Check Base64 early, but validate the decoded bytes instead of assuming every matching string is meaningful.

### 004 — Hexadecimal ASCII

The input is an even-length string containing only hexadecimal digits. Split it into byte pairs and decode the bytes as ASCII: `686d767b6d79666c61676973656173797d` becomes `hmv{myflagiseasy}`.

**Lesson:** Hex is a representation, not encryption. A quick byte conversion should precede heavier cryptanalysis.

### 007 — Mirrored text followed by Base64

First correct the upside-down or mirrored Unicode display. The normalized value is `SE1WezR2MWpOM3k0bX0=`, whose Base64 decoding is `HMV{4v1jN3y4m}`.

**Lesson:** Presentation can be a layer. Normalize direction, homoglyphs, and Unicode before identifying the underlying encoding.

### 010 — Ascii85/Base85

The punctuation-rich printable token is characteristic of the Base85 family. The article decodes it to `HMV{wrtzxcvfdghyt}`.

**Lesson:** Distinguish variants. Python exposes `base64.a85decode()` and `base64.b85decode()`; try the expected variant and require readable output rather than silently accepting garbage.

### 013 — Vigenère

Decrypt `MXV{BNRNKWPCEUSEX}` with repeating key `FLAG`, advancing the key over letters, to obtain `HMV{VIGNERECYPHER}`.

**Lesson:** Preserve punctuation and decide explicitly whether nonletters consume key positions. Different tools make different choices.

### 017 — Braille

Recognize the repeated six-dot cell structure as Braille, transcribe each cell, then map the cells to letters. The source reports `hmv{idontknowbraille}`.

**Lesson:** Transcription accuracy is the hard part. Keep cell boundaries and capture the original image before using an online symbol decoder.

### 023 — Cisco Type 7

Cisco Type 7 strings begin with a two-digit seed followed by hexadecimal pairs. Decoding `022E296D100B1622455D0A16031B130C11` with Cisco's fixed XOR table yields `HMV{myciscoflag}`.

**Lesson:** Type 7 is reversible obfuscation, not secure password hashing.

### 035 — Known-plaintext Vigenère with a custom alphabet

The challenge uses the alphabet `1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ`. Aligning supplied known plaintext with ciphertext reveals the repeating key `1F9S3SZ63TAS`; decrypting the remaining text exposes `HMV{h0w_d0_y0u_g37_th15}`.

**Why it works:** For alphabet indices modulo 36, Vigenère encryption is `C = P + K`. Therefore each aligned known pair reveals `K = C - P (mod 36)`.

### 044 — Bech32 identification

The `bc1q` prefix identifies a Bitcoin mainnet native SegWit address encoded with Bech32. The expected answer is `HMV{Bech32}`.

**Lesson:** This is format identification, not decoding a secret from the address. Bech32 uses a human-readable prefix, separator, a 5-bit-symbol data part, and a checksum; calling it merely “Base32” loses important structure.

### 046 — Recursive encodings and substitution

Join the supplied `x` and `y` fragments, Base64-decode the joined data, and inspect the output. It supplies a normal alphabet, a reversed alphabet, and another token. Translate with the normal alphabet mapped to its reverse. The result is another Base64 value, `SE1We3JlY3Vyc2lvbn0K`, which decodes to `HMV{recursion}`.

**Lesson:** After every decode, reassess the new data. Do not build a fixed “decode Base64 repeatedly” loop that ignores format changes between layers.

### 049 — PNG and Pigpen cipher

The long Base64 payload begins as image data after decoding. Save the bytes, verify the PNG signature, and inspect the image. The symbols use the Pigpen cipher; the source transcribes them as `NOTILLUMINATI`, giving `HMV{notilluminati}`.

**Evidence limit:** The visual transcription is artifact-dependent; the huge Base64 blob is omitted from this reference.

### 051 — Twin Hex

The string `2zx42j1ji5x05cj64f2lt5zc56a6w0` is identified by the source as Twin Hex. Decoding produces `HMV{4noth3r_C1pher}`.

**Lesson:** When a ciphertext is not ordinary hex despite a “hex” hint, inventory the actual character set and use the exact cipher variant named by the clue.

### 056 — Base2048

The many uncommon Unicode symbols indicate a high-radix Unicode encoding. A Base2048 decoder returns a sentence containing the answer `HMV{Base2048}`.

**Evidence limit:** Base2048 is not in Python's standard library and its alphabet is implementation-specific; preserve the exact Unicode input and identify the codec implementation used.

### 057 — Base65536

The same Unicode-density clue points to Base65536. The source reports decoded text `where_have_you_been_rpj7_:)`, wrapped as `HMV{where_have_you_been_rpj7_:)}`.

**Lesson:** Never normalize Unicode payloads before decoding. Copying through software that changes code points can destroy the data.

### 058 — D'ni numerals and base 25

Transcribe the D'ni numeral glyphs as digits `[1, 9, 6, 3, 18, 6]`. Interpret the sequence positionally in base 25:

```text
1×25⁵ + 9×25⁴ + 6×25³ + 3×25² + 18×25 + 6 = 13,377,331
```

The answer is `HMV{13377331}`.

**Lesson:** A fictional numeral system may encode digits in an unfamiliar base; glyph recognition and positional evaluation are separate steps.

### 061 — Base64, ZIP, binary, and ternary

Decode the outer Base64 and check magic bytes before choosing the next tool. The result is a ZIP archive. Its extracted text is binary-looking data; the next representation uses `t` as a separator between ternary groups. Convert each base-3 group to an integer, then to a character. The source reports `HMV{RPJ7_1_H0P3_Y0U_Cr4CK3D_17}`.

**Lesson:** Let signatures and alphabets drive each transition: Base64 characters → ZIP magic → binary text → ternary groups → ASCII.

### 062 — Code 128

Scan the supplied barcode as Code 128. The decoded seat text contains `HMV{1_l0v3_c0d3_128}`.

**Evidence limit:** This requires the original barcode image. If scanning fails, crop tightly, preserve horizontal bars, enlarge with nearest-neighbor scaling, and retry without lossy compression.

### 066 — Chinese-number hex and Rail Fence

The first layer represents hexadecimal nibbles using Chinese numerals for `0`–`9` and accented pinyin initials for `a`–`f`. Convert symbols to hex digits, decode the bytes, and inspect the scrambled plaintext. A seven-rail Rail Fence decode produces `HMV{Special_greetings_to_my_dear_Chinese_friends}`.

**Lesson:** Use the challenge's own mapping evidence. Accented pinyin is being used as a custom symbol table, not as a universal cipher standard.

### 068 — Unicode homoglyph steganography

The visible prose contains code-point differences among characters that look alike. A Unicode/homoglyph steganography decoder reveals the source-reported payload `hmvgreetings_from_green_br0ther`.

**Evidence limit:** The article does not show braces in the decoded payload. Keep it verbatim rather than inventing `HMV{...}` formatting.

### 069 — Nibble substitution from a known format

The byte sequence is not ordinary ASCII, but the hint gives a shape like `HM@....@`. Treat each hexadecimal nibble as a substituted symbol. Aligning the known positions reveals the table `0..f → @..O`; applying it yields `HM@HACK@`.

**Lesson:** This is a monoalphabetic substitution over nibbles inferred from known plaintext. It should not be described as direct hex-to-ASCII conversion.

### 071 — Known-plaintext substitution

The long ciphertext mirrors the structure of a public English article about Anonymous. Align it with the original prose to build a ciphertext-to-plaintext substitution map, then apply that map to the embedded token. The decrypted sentence is “is the best website for vulnerable virtual machines,” giving `HMV{is_the_best_website_for_vulnerable_virtual_machines}`.

**Lesson:** Normalize case and punctuation consistently, and reject conflicting letter mappings. A wrong alignment can appear plausible for several words before failing.

### 080 — Regex construction

Read the pattern as a string generator: literals contribute characters, capture groups contribute their chosen text, and backreferences repeat earlier captures. The intended construction gives `HMV{Regex_4_the_Win}`.

**Important ambiguity:** `[VHM]{3}` does not uniquely force `HMV`; it accepts any three-character combination from that set. The expected `HMV` prefix comes from the platform's flag convention, not from that character class alone.

### 081 — Whitespace binary and Morse

Inspect the file as bytes: it contains only space (`0x20`), tab (`0x09`), and newline (`0x0a`). Split it into three regions rather than decoding the whole file uniformly.

1. In the first and third regions, map space/tab to `0`/`1`, group rows into eight bits, and decode ASCII.
2. In the middle region, interpret the two whitespace symbols as Morse dot/dash and preserve the separators.
3. Concatenate the three decoded fragments.

The source reports:

```text
D0NT_W0RRY_GUY5_B3_B4CK_S00N!_G0TT4_T4K3_C4R3_0F_S0ME_BU51N355_AR0UND_H3R3:)
```

The article does not show a standard `HMV{...}` wrapper, so the text is retained exactly.

### 082 — Mixed UTF widths

The hint “8Universal 16Threads of 32Friendship” signals UTF-8, UTF-16, and UTF-32. Examine the bytes, segment the stream where code-unit width or byte-order patterns change, and decode each segment with the matching Unicode encoding. The stylized characters read `HMV{power_of_UTF}`.

**Lesson:** Do not decode the entire file under a single encoding. Check BOMs when present and infer endianness from zero-byte placement when absent.

### 087 — XOR-generated Rubik's Cube moves

Base64-decode the payload, then XOR it with the repeating key `kerszi`. The plaintext is a Rubik's Cube move sequence equivalent to:

```text
F R U' R' U' R U R' F'
```

Applying the moves to the challenge cube makes the white stickers form `T`; the source reports `flag{T}`.

**Evidence limit:** The final character depends on the cube's starting state and move convention. It cannot be verified from the move string alone.

### 089 — Base64, hex, reverse

Base64-decode the outer text. Treat the result as hexadecimal bytes, decode those bytes to text, then reverse the character order. The final result is `FLAG{D3c1ph3r1ng_1s_fun}`.

**Lesson:** Reversal should be the last stage because the intermediate text is visibly backward; reversing the raw encoded bytes would produce a different result.

## Reusable offline helpers

### Common text encodings

```python
import base64

def decode_common(value: str) -> None:
    raw = value.strip()
    candidates = {
        "hex": lambda: bytes.fromhex(raw),
        "base64": lambda: base64.b64decode(raw, validate=True),
        "ascii85": lambda: base64.a85decode(raw),
        "base85": lambda: base64.b85decode(raw),
    }
    for name, decode in candidates.items():
        try:
            print(name, decode())
        except (ValueError, UnicodeError):
            pass
```

### Vigenère with an explicit alphabet

```python
def vigenere_decrypt(ciphertext: str, key: str, alphabet: str) -> str:
    positions = {char: index for index, char in enumerate(alphabet)}
    output = []
    key_index = 0

    for char in ciphertext:
        if char not in positions:
            output.append(char)
            continue
        shift = positions[key[key_index % len(key)]]
        output.append(alphabet[(positions[char] - shift) % len(alphabet)])
        key_index += 1
    return "".join(output)
```

For Challenge 013 use `alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ"`. For Challenge 035 use its custom alphabet exactly as supplied.

### Cisco Type 7

```python
CISCO_XLAT = "dsfd;kfoA,.iyewrkldJKDHSUB"

def cisco_type7(value: str) -> str:
    seed = int(value[:2])
    encrypted = bytes.fromhex(value[2:])
    return "".join(
        chr(byte ^ ord(CISCO_XLAT[(seed + index) % len(CISCO_XLAT)]))
        for index, byte in enumerate(encrypted)
    )
```

### Base-N digits

```python
def from_digits(digits: list[int], base: int) -> int:
    value = 0
    for digit in digits:
        if not 0 <= digit < base:
            raise ValueError(f"digit {digit} is invalid for base {base}")
        value = value * base + digit
    return value

print(from_digits([1, 9, 6, 3, 18, 6], 25))  # 13377331
```

### Safe layered-decoding workflow

```python
from pathlib import Path
import base64

encoded = Path("challenge.txt").read_text(encoding="utf-8").strip()
stage1 = base64.b64decode(encoded, validate=True)
Path("stage1.bin").write_bytes(stage1)

print(stage1[:16].hex())
print(stage1[:16])
```

Inspect `stage1.bin` with `file`, a hex viewer, or a signature table before performing the next transformation. This preserves evidence and avoids corrupting binary data through text decoding.

## Analysis and corrections

### High-value recurring patterns

| Pattern | Challenges | Operational rule |
|---|---|---|
| Normalize presentation before decoding | 007, 068, 082 | Preserve original code points and determine whether appearance itself carries data. |
| Identify by alphabet and structure | 001, 004, 010, 056, 057 | Record character set, padding, length, and magic bytes before choosing a codec. |
| Reassess after every layer | 046, 049, 061, 066, 087, 089 | Treat each output as new evidence; do not assume the next layer repeats the last. |
| Use known plaintext carefully | 035, 069, 071 | Align exact positions, build a reversible map, and reject mapping conflicts. |
| Separate transcription from decoding | 017, 049, 058, 062 | Save the artifact, document glyph boundaries, then apply the symbolic decoder. |
| Distinguish recognition from decryption | 044, 080 | A format name or intended match may be the answer even when no hidden ciphertext exists. |

### Reliability notes

- Challenge 044 is specifically Bech32/native SegWit identification; “Base32” is too generic.
- Challenge 068's source-reported payload has no braces. Do not silently normalize it into a flag.
- Challenge 080's regex permits multiple three-letter prefixes; `HMV` is selected using challenge context.
- Challenge 081's source reports plaintext without an `HMV{...}` wrapper.
- Challenge 087 reports `flag{T}`, which differs from the usual HackMyVM prefix and therefore needs the original challenge for confirmation.
- Flags and capitalization are retained as shown by the decoded/source-reported outputs because challenge validators may be case-sensitive.

## Related vault pages

- [Cryptography Blueprint](../blueprints/Cryptography%20Blueprint.md)
- [dCode Cryptography Reference Index](dCode%20Cryptography%20Index.md)
- [REV Python Toolkit](../tools/REV%20Python%20Toolkit.md)
- [Temperance Challenge Solutions](../rev_source/Temperance%20Challenge%20Solutions.md)
- [Tools Index](../tools/Tools%20Index.md)

## Attribution

- Primary source: [f1agccc, “hackmyvm_challenge_crypto专题,” CSDN, 2025-05-05](https://blog.csdn.net/f1agccc/article/details/147709479).
- Platform: [HackMyVM challenges](https://hackmyvm.eu/challenges/).
- Source license shown by CSDN: [Creative Commons Attribution-ShareAlike 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
- This derivative study reference is shared under CC BY-SA 4.0. It paraphrases and reorganizes the source, adds verification labels and technical cautions, and omits the source's large embedded payloads and screenshots.
