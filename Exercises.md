# Exercises & Practice Hub

Central hub for all hands-on exercises, interactive crackmes, and CTF practice sets across all categories. Pick a track and start solving.

---

## ⚙️ Reverse Engineering Practice

### Interactive Crackmes

#### IDA Decompiler Z3 Crackme Challenges (Browser-based)
- **Source:** [Open in Browser](rev_source/gemini-code-1781600452949.html)
- **Difficulty:** 🟢 Easy
- **Format:** 10 interactive pseudo-C checks presented as a simulated Hex-Rays decompiler view. Enter your solution and get instant feedback.
- **Skills practiced:** Z3 solver scripting, `Int`/`BitVec` modeling, signed/unsigned reasoning, bit masking, modulo constraints, shift operations, XOR transforms.

| # | Function | Concept | Difficulty |
|---|---|---|---|
| 1 | `verify_key` | Basic simultaneous equations (3a + 2b = 180, a - b = 10) | 🟢 |
| 2 | `validate_serial` | Quadratic integer bounds (x² - 40x = 1200, x > 0) | 🟢 |
| 3 | `check_byte` | 8-bit signed overflow / sign extension (7k + 12 ≡ -46 mod 256) | 🟡 |
| 4 | `verify_str` | String checksum — character-by-character constraints with XOR | 🟡 |
| 5 | `bit_kernel` | Bit manipulation with AND/XOR masks (0xFF00, 0x00FF) | 🟡 |
| 6 | `array_checker` | 3-element array with sum/product/difference constraints | 🟡 |
| 7 | `modulo_lock` | Modulo relations with bounded search (mod 11 = 5, mod 13 = 3) | 🟡 |
| 8 | `shift_check` | Bit shifting — right shift and left shift with mask comparison | 🟠 |
| 9 | `multi_check` | Simultaneous 3-variable linear system (5x-3y+2z=29, etc.) | 🟠 |
| 10 | `final_boss` | Murmur-ish transform — XOR + rotate + add → target constant | 🟠 |

**How to practice:**
1. Open the [HTML challenge page](rev_source/gemini-code-1781600452949.html) in your browser.
2. Read the decompiled pseudo-C for each challenge.
3. Write a Python Z3 script to model the constraints and solve for valid input.
4. Enter the solution and verify with the built-in checker.

**Z3 solver template:**
```python
from z3 import *

# Example for Challenge 1
a = Int('a')
b = Int('b')
s = Solver()
s.add(3 * a + 2 * b == 180)
s.add(a - b == 10)
if s.check() == sat:
    m = s.model()
    print(f"{m[a]},{m[b]}")
```

---

### crackmes.one CTF 2026 (Binary Analysis)

Full progression-based challenge set from [crackmes.one CTF 2026](https://github.com/crackmesone/ctf-2026-challenges-public). Binaries are in `_source_crackmesone/`.

Detailed descriptions, hints, and progress tracker: **[REV Practice — crackmes.one CTF 2026](REV%20Practice.md)**

| Tier | Challenges | Skills |
|---|---|---|
| 🟢 Warm-Up | `wallpaper`, `cryptpad`, `Fatmike_02` | Strings, ltrace, GDB, basic patching, small PE/ELF |
| 🟡 Intermediate | `httpd`, `Fatmike`, `FLRSCRNSVR`, `moment` | Go binary RE, nanomites, JIT decryption, anti-tamper |
| 🟠 Advanced | `A_MatterOfTime`, `What did you type`, `Matryoshka v2` | AES key/IV recovery, timestamp brute-force, nested unpacking |
| 🔴 Expert | `connected`, `FlipVM` | Network protocol RE, custom VM, modified Kuznyechik cipher |

---

### Solved Writeups & Study Material (rev_source)

Reference writeups for reverse engineering techniques. Study these after attempting challenges to learn patterns.

| File | Challenge / Topic | Key Techniques |
|---|---|---|
| [bitmap.md](rev_source/bitmap.md) | IOCCC28 one-liner (PBM bitmap) | Magic division constants, bit recovery, row/column mapping |
| [NMTE-4667.md](rev_source/NMTE-4667.md) | Matrix multiplication disguise | Static equation extraction, pseudoinverse, Z3 fallback |
| [restlessness.md](rev_source/restlessness.md) | macOS artifact deobfuscation | Zsh alias chains, Base64/hex/ROT pipelines, plist inspection |
| [my-favorite-ingredient](rev_source/writeip_my-favorite-ingredient.md) | GPN CTF — matrix flag checker | 64×64 linear system mod 256, Z3 `BitVec` solving |

External writeup snapshots available offline in [`rev_source/linked_pages/`](rev_source/linked_pages/).

---

## 🌐 Web Exploitation Practice

*(Add your web CTF solves and exercises here as you complete them.)*

### Suggested Practice Sources
- [picoCTF Web Challenges](_source_picoctf_cajac/) — Local mirror of picoCTF writeups (2019–2025).
- [Sec-Fortress Writeups](_source_sec_fortress/) — HackTheBox, TryHackMe, and CTF web challenge writeups.
- [HackMyVM Writeups](_source_hackmyvm_writeups/) — Boot2root machine writeups with web components.

---

## 🖥️ Machine Exploitation Practice

*(Add your machine solves and logs here as you complete them.)*

### Suggested Practice Sources
- [HackMyVM Writeups](_source_hackmyvm_writeups/) — Linux/Windows boot2root walkthroughs.
- [TryHackMe Writeups (0xb0b)](_source_0xb0b_tryhackme/) — TryHackMe room solutions.
- [TryHackMe Writeups (cajac)](_source_tryhackme_cajac/) — Additional TryHackMe coverage.

---

## 🔐 Cryptography Practice

*(Add your crypto CTF solves here as you complete them.)*

### Suggested Practice Sources
- [Temperance Levels](_source_temperance/) — 33 progressive Python-based crypto/encoding challenges (`levelx00.py` – `levelx32.py`).
- [picoCTF Crypto Challenges](_source_picoctf_cajac/) — Encoding chains, XOR, RSA, and substitution ciphers.

---

## 🖼️ Steganography Practice

*(Add your stego solves here as you complete them.)*

---

## Progress Overview

| Category | Active Exercise Sets | Status |
|---|---|---|
| REV — Z3 Crackmes (Browser) | 10 challenges | Ready |
| REV — crackmes.one CTF 2026 | 12 challenges + 3 Z3 tiers | Ready |
| REV — Solved Writeups | 4 study references | Ready |
| Web Exploitation | Placeholder | Awaiting your solves |
| Machine Exploitation | Placeholder | Awaiting your solves |
| Cryptography | Placeholder | Awaiting your solves |
| Steganography | Placeholder | Awaiting your solves |

---

## Related

- [REV Practice — crackmes.one CTF 2026](REV%20Practice.md)
- [Reverse Engineering Playbook](Reverse%20Engineering%20Playbook.md)
- [H4G Training Hub](H4G%20Training.md)
- [Challenge Use Cases](references/Challenge%20Use%20Cases.md)
- [REV Python Toolkit](tools/REV%20Python%20Toolkit.md)
