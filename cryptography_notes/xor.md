---
tags: [ctf, crypto, xor]
status: reference
---

# XOR Cipher

## Summary
Bitwise XOR used as a stream cipher. `C = P XOR K`. Trivially broken when key is short/repeated, key is reused, or any plaintext is known. Very common in CTF warm-ups and obfuscation layers.

## How it works
- Single-byte key: `C[i] = P[i] XOR k`
- Repeating key: `C[i] = P[i] XOR K[i % len(K)]`
- OTP (truly random, never reused key = len(P)): theoretically unbreakable

## Weaknesses / Attack Angles
- **Single-byte brute force**: 256 candidates, score by English letter frequency
- **Known plaintext**: `K = P XOR C` (if you know file header, flag format `CTF{`, etc.)
- **Key length detection**: index of coincidence (IoC) or Kasiski test on repeating-key XOR
- **Multi-byte brute force**: split ciphertext into `keylen` groups, each is single-byte XOR
- **Nonce reuse (CTR/stream)**: `C1 XOR C2 = P1 XOR P2` → crib-drag
- **Null bytes**: if plaintext contains `\x00`, ciphertext bytes directly reveal key bytes

## Tools
- `xortool` — key length detection + multi-byte key recovery
- `CyberChef` — quick single-byte / multi-byte XOR in browser
- Python `itertools` / custom scorer

## Quick Snippet

```python
# --- Single-byte XOR brute force ---
from string import printable

ct = bytes.fromhex("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736")

def score(s):
    freq = "etaoin shrdlu"
    return sum(c.lower() in freq for c in s if chr(c) in printable)

best = max(range(256), key=lambda k: score(bytes(b ^ k for b in ct)))
print(f"Key: {best:#04x}", bytes(b ^ best for b in ct))

# --- Known plaintext key recovery ---
ct      = bytes.fromhex("...")
known   = b"CTF{"          # known start of plaintext
key     = bytes(c ^ p for c, p in zip(ct, known))
print("Key bytes:", key)

# --- Repeating-key XOR encrypt/decrypt ---
def xor_key(data: bytes, key: bytes) -> bytes:
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))

# --- Key length via IoC ---
def ioc(data):
    n = len(data)
    freq = [data.count(i) for i in range(256)]
    return sum(f*(f-1) for f in freq) / (n*(n-1)) if n > 1 else 0

ct = bytes.fromhex("...")
for kl in range(1, 33):
    avg_ioc = sum(ioc(ct[i::kl]) for i in range(kl)) / kl
    print(f"keylen={kl:2d}  IoC={avg_ioc:.4f}")
# English IoC ≈ 0.065 — look for peak

# --- Multi-byte key recovery (after finding key length) ---
key_len = 6
key = bytes(
    max(range(256), key=lambda k: score(bytes(b ^ k for b in ct[i::key_len])))
    for i in range(key_len)
)
print("Key:", key)
print(xor_key(ct, key))
```

## Spot it in a challenge when...
- Binary/hex blob provided with no other context (likely XOR obfuscated)
- Flag format `CTF{` appears as known plaintext → instant key partial
- Ciphertext same length as key hint → OTP gone wrong somewhere
- Two ciphertexts of same length and "same key" mentioned → nonce reuse

## References
- [xortool GitHub](https://github.com/hellman/xortool)
- [CryptoHack XOR challenges](https://cryptohack.org/challenges/general/)

## Related
- [[aes]]
- [[vigenere]]
