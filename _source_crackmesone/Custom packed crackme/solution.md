# OUT.exe — Static Reverse Engineering Writeup (No Execution)

Date: 2026-02-25  
Method: **Static-only** (Binary Ninja + offline decoding/decompression + manual logic lift)

---

## 1) Scope

This analysis was performed with a strict non-execution policy:
- no running the sample
- no debugger runtime
- no dynamic tracing

Objective:
- recover the real key accepted by the challenge logic
- provide a fully reproducible static path

---

## 2) Sample fingerprint

- Filename: `OUT.exe`
- SHA256: `99279210c3eb9bd8302125d5651d0dcc1fe1a52a95412792c662963cb3339995`

---

## 3) High-level architecture

`OUT.exe` is not a direct checker. It is a staged loader/validator:

1. Bootstrap gate (`_start`) with anti-tamper style transform checks.
2. VM-driven validator (`sub_1400089C0` + `sub_140009940`) that executes 4 encrypted bytecode blobs.
3. VM external mode calls (modes 1..14) implement a loader pipeline.
4. That pipeline extracts/decrypts/decompresses a hidden stage, then runs validation code from it.

Because execution is forbidden, the stage extraction + logic recovery was replicated statically.

---

## 4) Embedded footer and payload extraction

At end-of-file there is a 0x20-byte trailer:

- Magic: `EPSTEIN3`
- `var_188 = 0x3AD`
- `var_180 = 0x0A00`
- mode byte = `0x02`
- extra length = `0x0C`

From these fields:
- encrypted payload length = `0x3AD` bytes
- extra block length = `0x0C` bytes (nonce material)

---

## 5) AES-GCM decryption layer (static)

Mode `0x02` path uses BCrypt APIs (resolved dynamically), with deobfuscated identifiers:
- `bcrypt.dll`
- `BCryptOpenAlgorithmProvider`
- `BCryptSetProperty`
- `BCryptGetProperty`
- `BCryptGenerateSymmetricKey`
- `BCryptDecrypt`
- `BCryptDestroyKey`
- `BCryptCloseAlgorithmProvider`

Wide properties deobfuscate to:
- `AES`
- `ObjectLength`
- `ChainingMode`
- `ChainingModeGCM`

So layer-1 payload decrypt is AES-GCM.

### Key derivation
A custom 32-byte key is derived from:
- static seed at `data_14001E320` (32 bytes)
- trailing extra block (12-byte nonce source)

The KDF is a 64-bit rotate/mix routine (`sub_140002B60`) producing a 32-byte key.

Recovered material:
- Nonce (12 bytes): `91c0d9f9ac4daa6196b0ff4f`
- Derived AES key: `dbf382cbb3372e687a0724ea906f6eb68d98ba769d03a79da8d48ca489e3ff72`

Payload structure:
- ciphertext = first `0x395` bytes
- tag = final `0x10` bytes

AES-GCM decrypt output length: **925** bytes.

---

## 6) LZMA2 decompression layer (static)

A second transform is applied by internal decoder logic (`sub_140001D80` / `sub_140019200`).

Parameter byte `0x16` (from footer metadata path) maps to LZMA2 dictionary formula:

`dict_size = ((prop & 1) + 2) << ((prop >> 1) + 11)`

For `prop=0x16`:
- `dict_size = 0x800000`

Using LZMA2 raw decompression on the 925-byte decrypted stream yields:
- output size: **2560 bytes**
- output begins with `MZ` (valid PE)

Recovered inner PE hash:
- SHA256: `b3f77138c0d289b6c03d0dd78eee5148aa27e226ade5d1f3ef2d7f716e2863dc`

---

## 7) Inner checker logic recovery

The unpacked PE is a compact console checker using:
- `ReadFile` from stdin
- `WriteFile` for prompt/result

Validation logic (all static):

### Stage A
- input length must be exactly 16
- chars must be alphanumeric (`0-9A-Za-z`)

### Stage B (global constraints)
- sum of all 16 bytes must be `0x526` (1318)
- 32-bit rolling transform must end as `0x780E293F`

### Stage C (bytewise affine-xor relation)
For each `i in [0..15]`:

`((input[i] + i*0x0D) & 0xFF) XOR arr1[i] == arr2[i]`

with:
- `arr1 = 3a c1 17 8e 55 29 b4 6d 90 4f 22 d8 71 0c ae 5b`
- `arr2 = 7c ba 7d 1c 3f 51 77 df 0e e3 d7 1e 8f 2f a1 ae`

This directly resolves all 16 bytes.

### Stage D (cross-byte consistency checks)
Additional checks on selected indices (differences/sums/xor/equality) are satisfied by the same resolved candidate.

---

## 8) Recovered correct key

**Final accepted key:**

`FnPk67uW67s7bzY2`

Verified statically against all recovered constraints:
- length/alnum ✅
- sum/hash state ✅
- bytewise table equations ✅
- final cross-byte equations ✅

---

## 9) Conclusion

The key was recovered end-to-end using static reverse engineering only:
- container parsing
- custom KDF reconstruction
- AES-GCM decryption
- LZMA2 decompression
- inner checker lifting and constraint solving

No binary execution was required at any stage.
