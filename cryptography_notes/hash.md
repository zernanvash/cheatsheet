---
tags: [ctf, crypto, hash]
status: reference
---

# Hash Functions

## Summary
One-way functions: `H(m) → digest`. Used for integrity, MACs, passwords. CTF attacks exploit construction flaws (Merkle-Damgård length extension), weak MAC patterns (`H(key||msg)`), or precomputed collision databases.

## How it works
- **Merkle-Damgård** (MD5, SHA-1, SHA-256): processes blocks sequentially, state carried forward → length extension possible
- **SHA-3 / BLAKE**: sponge construction → immune to length extension
- **HMAC**: `H(key XOR opad || H(key XOR ipad || msg))` — safe MAC pattern

## Weaknesses / Attack Angles
- **Length extension**: `H(secret || msg)` MAC scheme → append data and forge valid MAC without knowing secret
- **Hash collision (MD5/SHA-1)**: identical hash for different inputs → SHAttered, HashClash
- **Preimage via rainbow tables**: unsalted password hashes → crackstation.net, hashcat
- **Hash-as-MAC (`H(key||msg)`)**: length extension
- **Weak entropy seed**: if PRNG seeded with timestamp, brute-force seed → reproduce hash
- **Truncated hash comparison**: `h[:8] == expected[:8]` → birthday attack far cheaper

## Tools
- `hashpumpy` — Python length extension attack
- `hash_extender` — CLI length extension (Skullsecurity)
- `hashcat` — GPU password cracking
- `john` — CPU hash cracking
- `hashid` / `haiti` — identify hash type from digest

## Quick Snippet

```python
# --- Identify hash length from digest length ---
digest = "5d41402abc4b2a76b9719d911017c592"
lengths = {32: "MD5", 40: "SHA-1", 56: "SHA-224", 64: "SHA-256", 96: "SHA-384", 128: "SHA-512"}
print(lengths.get(len(digest), "Unknown"))

# --- Length Extension with hashpumpy ---
# pip install hashpumpy
import hashpumpy

# MAC = SHA256(secret || original_data), secret length known/guessed
original_data    = b"count=10&lat=37.351&user_id=1&long=-119.827&waffle=eggo"
mac_hex          = "6d5f807e23db210bc254a28be2d6759a0f5f5d99"   # SHA1 example
secret_length    = 14
data_to_append   = b"&waffle=liege"

new_mac, new_msg = hashpumpy.hashpump(mac_hex, original_data, data_to_append, secret_length)
print(f"New MAC : {new_mac}")
print(f"New msg : {new_msg.hex()}")

# --- Manual SHA-256 length extension (conceptual) ---
# Use hashlib to restore internal state from known digest
# then continue hashing appended data (hashpumpy does this for you)

# --- Password hash cracking (hashcat modes) ---
# MD5         : hashcat -m 0   hashes.txt wordlist.txt
# SHA-1       : hashcat -m 100 hashes.txt wordlist.txt
# bcrypt      : hashcat -m 3200 hashes.txt wordlist.txt
# SHA-256     : hashcat -m 1400 hashes.txt wordlist.txt

# --- HMAC (correct pattern, for reference) ---
import hmac, hashlib
mac = hmac.new(key, msg, hashlib.sha256).hexdigest()
```

## Spot it in a challenge when...
- MAC is `H(secret || input)` — check for length extension
- Digest looks like 32/40/64 hex chars → identify algo
- "Forgot password" token is just `MD5(username + timestamp)` → brute seed
- Challenge says "prove integrity" and gives you the hash — check if MAC vs bare hash

## References
- [hash_extender (Skullsecurity)](https://github.com/iagox86/hash_extender)
- [SHAttered MD5/SHA-1 collisions](https://shattered.io/)

## Related
- [[aes]]
- [[rsa]]
