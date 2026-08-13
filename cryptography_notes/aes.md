---
tags: [ctf, crypto, aes]
status: reference
---

# AES

## Summary
Block cipher, 128-bit blocks, key sizes 128/192/256 bit. In CTFs the cipher itself is never broken — attacks target the **mode of operation** or **IV/key reuse**.

## How it works
- **ECB**: each block encrypted independently → identical plaintext blocks → identical ciphertext blocks
- **CBC**: `Cᵢ = E(Pᵢ XOR Cᵢ₋₁)`, decrypt: `Pᵢ = D(Cᵢ) XOR Cᵢ₋₁`; IV used for block 0
- **CTR**: keystream `E(nonce || counter)` XORed with plaintext → stream cipher
- **GCM**: CTR + GHASH authentication tag; nonce reuse is catastrophic

## Weaknesses / Attack Angles

| Mode | Attack | Condition |
|---|---|---|
| **ECB** | Block swapping / oracle | Two identical 16-byte plaintext blocks → identical ciphertext |
| **ECB** | Byte-at-a-time | Attacker controls prefix/suffix of plaintext before unknown secret |
| **CBC** | Padding Oracle | Decryption oracle leaks whether PKCS#7 padding is valid |
| **CBC** | Bit-flip | Modify `Cᵢ₋₁` bits → predictable XOR flip in `Pᵢ` |
| **CBC** | IV = Key | If IV == key, recovering IV recovers key |
| **CTR** | Nonce reuse XOR | Two plaintexts encrypted with same nonce → XOR them → XOR of plaintexts |
| **GCM** | Nonce reuse | Recover auth key `H`, forge tags |

## Tools
- `pycryptodome` — `AES.new(key, AES.MODE_CBC, iv).decrypt(ct)`
- `padbuster` — automated padding oracle exploitation
- `pwntools` — socket interaction for oracle challenges

## Quick Snippet

```python
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

key = b'\x00' * 16   # replace with actual key
iv  = b'\x00' * 16

# --- ECB detect: look for repeated 16-byte blocks ---
ct = bytes.fromhex("...")
blocks = [ct[i:i+16] for i in range(0, len(ct), 16)]
print("ECB detected" if len(blocks) != len(set(blocks)) else "Not ECB")

# --- ECB byte-at-a-time (skeleton) ---
# Incrementally extend known prefix, observe when block boundary shifts
def ecb_oracle(plaintext): ...   # call remote/local encrypt

# --- CBC Decrypt (known key+iv) ---
cipher = AES.new(key, AES.MODE_CBC, iv)
pt = unpad(cipher.decrypt(ct), 16)
print(pt)

# --- CBC Bit-flip: flip byte at position `pos` in ciphertext to change plaintext ---
def cbc_bitflip(ct: bytes, pos: int, old_byte: int, new_byte: int) -> bytes:
    ct = bytearray(ct)
    ct[pos - 16] ^= old_byte ^ new_byte   # flip in previous block
    return bytes(ct)

# --- Padding Oracle (manual single-block) ---
def padding_oracle_decrypt_block(oracle, prev_block, target_block):
    """oracle(iv, ct) -> True if padding valid"""
    inter = bytearray(16)
    for i in range(15, -1, -1):
        pad_byte = 16 - i
        for guess in range(256):
            iv_try = bytearray(prev_block)
            iv_try[i] = guess
            for j in range(i+1, 16):
                iv_try[j] = inter[j] ^ pad_byte
            if oracle(bytes(iv_try), target_block):
                inter[i] = guess ^ pad_byte
                break
    return bytes(x ^ y for x, y in zip(inter, prev_block))

# --- CTR nonce-reuse XOR trick ---
ct1 = bytes.fromhex("...")   # E(key, nonce) XOR pt1
ct2 = bytes.fromhex("...")   # E(key, nonce) XOR pt2
xored = bytes(a ^ b for a, b in zip(ct1, ct2))  # = pt1 XOR pt2
# now use crib-dragging to recover both plaintexts
```

## Spot it in a challenge when...
- Ciphertext length is a multiple of 16
- Repeated blocks in ciphertext → ECB
- "Valid/invalid padding" error exposed → padding oracle
- Same nonce used for multiple encryptions in CTR/GCM
- `iv == key` or IV is fixed/predictable

## References
- [PyCryptodome AES docs](https://pycryptodome.readthedocs.io/en/latest/src/cipher/AES.html)
- [Padding Oracle explained (Robert Heaton)](https://robertheaton.com/2013/07/29/padding-oracle-attack/)

## Related
- [[xor]]
- [[padding-oracle]]
