---
tags: [ctf, crypto, classical]
status: reference
---

# Classical Ciphers

## Summary
Pre-computer substitution/transposition schemes. Always solvable with frequency analysis or brute force. Common in CTF intro/easy tiers and steganography layers.

## How it works (quick table)

| Cipher | Key | Decrypt method |
|---|---|---|
| **Caesar** | shift n (0-25) | brute 26, freq analysis |
| **ROT13** | shift 13 | just apply ROT13 again |
| **Atbash** | none | A↔Z, B↔Y, … (self-inverse) |
| **Playfair** | keyword 5×5 grid | digraph substitution |
| **Rail Fence** | rail count | reconstruct zigzag pattern |
| **Columnar transposition** | keyword → column order | reorder columns |
| **Baconian** | A=AAAAA B=AAAAB | 5-bit binary alphabet |
| **Polybius square** | 5×5 grid | coordinate lookup |
| **Morse** | — | decode dots/dashes |

## Weaknesses / Attack Angles
- Single-char or digraph frequency analysis cracks almost all substitution ciphers
- Letter `e` = most common in English (~12.7%), `th` = most common digraph
- CyberChef "Magic" or dcode.fr auto-identification handles most classical ciphers

## Tools
- `dcode.fr` — identify + crack almost any classical cipher online
- `CyberChef` — ROT, Atbash, Morse, Baconian, Rail Fence all built-in
- `quipqiup.com` — automated substitution cipher solver

## Quick Snippet

```python
import string

ALPHA = string.ascii_uppercase

# --- Caesar brute force ---
ct = "Khoor Zruog"
for shift in range(26):
    pt = "".join(
        ALPHA[(ALPHA.index(c.upper()) - shift) % 26] if c.upper() in ALPHA else c
        for c in ct
    )
    print(f"shift={shift:2d}: {pt}")

# --- Atbash ---
def atbash(text):
    return "".join(
        ALPHA[25 - ALPHA.index(c.upper())] if c.upper() in ALPHA else c
        for c in text
    )

# --- Rail Fence decode ---
def rail_fence_decode(ct, rails):
    n = len(ct)
    # determine row lengths
    cycle = 2 * (rails - 1)
    lengths = [0] * rails
    for i in range(n):
        r = i % cycle
        r = r if r < rails else cycle - r
        lengths[r] += 1
    # split ciphertext into rows
    rows, idx = [], 0
    for l in lengths:
        rows.append(list(ct[idx:idx+l]))
        idx += l
    # read off in zigzag order
    result, indices = [], [0] * rails
    for i in range(n):
        r = i % cycle
        r = r if r < rails else cycle - r
        result.append(rows[r][indices[r]])
        indices[r] += 1
    return "".join(result)

# --- Baconian decode ---
BACONIAN = {f"{i:05b}".replace("0","A").replace("1","B"): ALPHA[i] for i in range(26)}
def baconian_decode(text):
    text = text.upper().replace(" ", "")
    return "".join(BACONIAN.get(text[i:i+5], "?") for i in range(0, len(text), 5))
```

## Spot it in a challenge when...
- Text looks like English but every letter is shifted uniformly → Caesar
- Only A and B letters (or dots/dashes, 0s/1s) → Baconian / Morse
- Pairs of numbers (11, 23, …) → Polybius
- Scrambled text with all original letters present → transposition
- `dcode.fr` "Cipher Identifier" → paste ciphertext, let it guess

## References
- [dcode.fr cipher identifier](https://www.dcode.fr/cipher-identifier)
- [CyberChef Magic](https://gchq.github.io/CyberChef/#recipe=Magic(3,false,false,''))

## Related
- [[vigenere]]
- [[xor]]
