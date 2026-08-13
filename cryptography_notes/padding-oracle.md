---
tags: [ctf, crypto, aes, padding-oracle]
status: reference
---

# Padding Oracle Attack

## Summary
If a decryption endpoint reveals whether PKCS#7 padding is valid (even via timing or error message differences), an attacker can decrypt any ciphertext **without the key** — one byte at a time, ~256 requests per byte.

## How it works
- PKCS#7 padding: last block padded with `\x01`, `\x02\x02`, `\x03\x03\x03`, etc.
- CBC decrypt: `P[i] = D(C[i]) XOR C[i-1]`
- Flip `C[i-1][j]` → changes `P[i][j]` predictably → probe for valid padding byte

## Attack Steps
1. Isolate target block `C[i]` and its predecessor `C[i-1]`
2. For each byte position `j` (right to left):
   - Brute 0–255 for `C[i-1][j]`; send to oracle
   - Valid padding → found `D(C[i])[j]` intermediate byte
   - `P[i][j] = D(C[i])[j] XOR original_C[i-1][j]`
3. Repeat for each block; recover full plaintext

## Tools
- `padbuster` — CLI: `padbuster <URL> <ciphertext_b64> <blocksize>`
- `python-paddingoracle` — Python library for custom oracles
- Custom Python (below) for CTFs with non-HTTP oracles

## Quick Snippet

```python
import requests   # replace with socket/pwntools as needed

BLOCK = 16

def oracle(iv: bytes, ct: bytes) -> bool:
    """Return True if server says padding valid."""
    # Example HTTP oracle:
    r = requests.get("http://$URL/decrypt", params={
        "iv": iv.hex(), "ct": ct.hex()
    })
    return "PaddingException" not in r.text   # adapt to challenge

def decrypt_block(prev_block: bytes, target_block: bytes) -> bytes:
    inter = bytearray(BLOCK)   # D(target_block) — intermediate values
    for byte_pos in range(BLOCK - 1, -1, -1):
        pad_byte = BLOCK - byte_pos
        for guess in range(256):
            iv_try = bytearray(BLOCK)
            # set already-solved bytes to produce correct padding
            for k in range(byte_pos + 1, BLOCK):
                iv_try[k] = inter[k] ^ pad_byte
            iv_try[byte_pos] = guess
            if oracle(bytes(iv_try), target_block):
                # guess ^ pad_byte = D(target)[byte_pos]
                inter[byte_pos] = guess ^ pad_byte
                break
    # XOR intermediate with original prev block to get plaintext
    return bytes(i ^ p for i, p in zip(inter, prev_block))

def decrypt_cbc(iv: bytes, ct: bytes) -> bytes:
    blocks = [ct[i:i+BLOCK] for i in range(0, len(ct), BLOCK)]
    chain  = [iv] + blocks
    pt = b""
    for i in range(1, len(chain)):
        pt += decrypt_block(chain[i-1], chain[i])
    # strip PKCS#7
    pad = pt[-1]
    return pt[:-pad]

# Usage
iv = bytes.fromhex("...")
ct = bytes.fromhex("...")
print(decrypt_cbc(iv, ct))
```

## Spot it in a challenge when...
- Web endpoint returns different error for bad padding vs bad data
- Timing difference between "invalid padding" and "invalid data"
- Challenge title: "padding", "oracle", "valid/invalid", "CBC"
- Error message leaks: `PaddingException`, `Invalid padding`, `Bad decrypt`

## References
- [PadBuster](https://github.com/AonCyberLabs/PadBuster)
- [Robert Heaton's explanation](https://robertheaton.com/2013/07/29/padding-oracle-attack/)

## Related
- [[aes]]
