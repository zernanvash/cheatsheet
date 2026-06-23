# crackme_goodlucklol — Writeup

**Platform:** Windows x64  
**Tools:** IDA Pro 9.3, Python  

## First Look

We're greeted with a classic prompt:

```
Welcome to the Secure Login System
Password:
```

Wrong password gives "Access denied!", correct one — "Access granted!" followed by the flag. Simple enough, let's dig in.

From the PDB path found in strings (`crackme_SBHA16\securelogin.pdb`) we can tell the author named the project "SBHA16" — probably "Software Based Hardware Abstraction, 16 bytes". This will make sense later.

## How main works

After reading the password string, `main` does something unexpected — it doesn't pass the raw string to the checker. Instead it:

1. Allocates a 128-byte buffer, zeroes it out.
2. Converts the password string into **individual bits** — each character becomes 8 bytes (MSB first), each being `0x00` or `0x01`. So the buffer holds the binary representation of the password. 128 bits = 16 characters max.
3. Passes this bit-buffer to the check function.
4. If the check passes, it XOR-decrypts a 47-byte embedded blob using `enc[i] ^ password[i % password_length]` and prints the flag.

Key takeaway: we need the real password, patching the check won't help since the password is the XOR key for the flag.

## The Check Function — 8KB of Chaos

The checker (`sub_1400102F0`) is massive — 8037 bytes. Looks scary, but once you understand the structure, it's actually straightforward.

**Step 1 — Shuffle.** It reads all 128 bytes from the bit-buffer and scatters them into different local stack variables. Just a permutation to confuse the reverser.

**Step 2 — NOT.** 71 of these variables go through a tiny function that does logical NOT: if the byte is zero, return 1; otherwise return 0.

**Step 3 — AND chain.** All 128 values (71 NOT-ed + 57 originals) are chained together through a logical AND function: `AND(a, b) = (a != 0 && b != 0) ? 1 : 0`. This folds 128 values down to a single result byte.

For the final AND to be 1, **every single input** to the chain must be non-zero:
- The 71 NOT-ed bits must have been 0 originally (so NOT returns 1)
- The 57 non-NOT-ed bits must have been 1 originally (non-zero passes AND)

This means the check simply verifies that **specific bit positions are 1 and the rest are 0**. It's a fixed bit-pattern check — essentially the password is hardcoded, just very obfuscated.

## Extracting the Password

I wrote an IDA script to parse the function automatically and map out which of the 128 bit positions must be 0 vs 1. Then reconstructed the password byte by byte:

```python
nonzero_positions = {2, 5, 10, 13, 15, 17, 19, 20, 23, 25, 26, 31, 33, 34,
    38, 39, 41, 42, 44, 46, 47, 49, 50, 52, 55, 57, 58, 60, 61, 62, 65, 66,
    69, 70, 71, 74, 75, 79, 82, 83, 86, 90, 91, 94, 95, 98, 99, 101, 106,
    107, 108, 111, 114, 115, 122, 123, 127}

bits = [0] * 128
for pos in nonzero_positions:
    bits[pos] = 1

password = []
for i in range(16):
    byte_val = 0
    for j in range(8):
        byte_val = (byte_val << 1) | bits[i * 8 + j]
    password.append(byte_val)

print(bytes(password).rstrip(b'\x00'))
# b'$%Yacking1234901'
```

## Result

```
Password: $%Yacking1234901
Access granted!
dzctf(SoftwareBasedHardwareAbstraction_is_cool)
```

**Password:** `$%Yacking1234901`  
**Flag:** `dzctf(SoftwareBasedHardwareAbstraction_is_cool)`

## Summary

The crackme converts the password to a 128-bit binary representation, then uses an 8KB function built entirely out of NOT and AND gates to check every single bit against a hardcoded pattern. It's essentially a hardware-style combinational logic circuit implemented in software — which explains the name "Software Based Hardware Abstraction". Clever idea, but once you understand the building blocks, the whole thing collapses into a simple bit-pattern extraction.
