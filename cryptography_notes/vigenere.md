---
tags: [ctf, crypto, classical, vigenere]
status: reference
---

# Vigenère Cipher

## Summary
Polyalphabetic substitution: `C[i] = (P[i] + K[i % keylen]) mod 26`. Appears in classical crypto / easy CTF tiers. Key length → break into Caesar ciphers.

## How it works
- Each character shifted by corresponding key character (cyclic)
- Equivalent to `keylen` interleaved Caesar ciphers
- Alphabet usually A-Z (mod 26) but sometimes extended to printable ASCII (mod 95)

## Weaknesses / Attack Angles
- **Kasiski test**: find repeated trigrams/bigrams → distances → GCD → key length
- **Index of Coincidence (IoC)**: for correct key length, each column IoC ≈ 0.065 (English)
- **Frequency analysis per column**: once key length known, each column is single-shift Caesar → pick shift with best freq match
- **Known plaintext**: `K[i] = (C[i] - P[i]) mod 26`
- **Short key**: if key ≤ 4 chars, brute force all possibilities

## Tools
- `dcode.fr/vigenere-cipher` — online solve with auto key-length detection
- `CyberChef` — Vigenere decode module
- `xortool` — handles XOR variant (bytes instead of mod 26)

## Quick Snippet

```python
import string
from collections import Counter

ALPHA = string.ascii_uppercase

def vigenere_decrypt(ct: str, key: str) -> str:
    ct  = ct.upper().replace(" ", "")
    key = key.upper()
    return "".join(
        ALPHA[(ALPHA.index(c) - ALPHA.index(key[i % len(key)])) % 26]
        for i, c in enumerate(ct) if c in ALPHA
    )

# --- IoC for key length detection ---
def ioc(text):
    n = len(text)
    freq = Counter(text)
    return sum(v*(v-1) for v in freq.values()) / (n*(n-1)) if n > 1 else 0

def find_key_length(ct, max_kl=20):
    ct = ct.upper()
    ct = [c for c in ct if c in ALPHA]
    scores = {}
    for kl in range(1, max_kl+1):
        cols = ["".join(ct[i::kl]) for i in range(kl)]
        scores[kl] = sum(ioc(c) for c in cols) / kl
    return sorted(scores, key=scores.get, reverse=True)[:5]

# --- Frequency attack per column ---
ENGLISH_FREQ = "ETAOINSHRDLCUMWFGYPBVKJXQZ"

def crack_column(col):
    best_shift, best_score = 0, -1
    for shift in range(26):
        decrypted = "".join(ALPHA[(ALPHA.index(c) - shift) % 26] for c in col if c in ALPHA)
        score = sum(decrypted.count(ch) * (26 - i) for i, ch in enumerate(ENGLISH_FREQ))
        if score > best_score:
            best_score, best_shift = score, shift
    return ALPHA[best_shift]

ct = "LXFOPVEFRNHR"
key_len = find_key_length(ct)[0]
ct_clean = [c for c in ct.upper() if c in ALPHA]
key = "".join(crack_column(ct_clean[i::key_len]) for i in range(key_len))
print(f"Key: {key}")
print(vigenere_decrypt(ct, key))
```

## Spot it in a challenge when...
- Ciphertext is only alphabetic characters, uniform-looking
- Challenge says "Caesar-like" or "polyalphabetic"
- Letter frequency is flatter than natural English but not random
- Key hint provided (common word, CTF theme)

## References
- [dcode.fr Vigenère solver](https://www.dcode.fr/vigenere-cipher)
- [Kasiski test explained](https://en.wikipedia.org/wiki/Kasiski_examination)

## Related
- [[xor]]
- [[classical-ciphers]]
