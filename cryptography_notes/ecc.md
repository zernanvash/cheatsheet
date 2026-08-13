---
tags: [ctf, crypto, ecc]
status: reference
---

# Elliptic Curve Cryptography (ECC)

## Summary
Public-key crypto on elliptic curves `y² = x³ + ax + b mod p`. Security = ECDLP (elliptic curve discrete log problem). CTF attacks target weak curves, bad randomness in ECDSA, or implementation leaks.

## How it works
- Point addition + scalar multiplication: `Q = k × G` (public key)
- ECDLP: given `G`, `Q`, find `k` — hard on good curves
- **ECDH**: shared secret = `k_A × Q_B = k_B × Q_A`
- **ECDSA sign**: `r = (k×G).x mod n`, `s = k⁻¹(hash + r×d) mod n`
- **ECDSA verify**: recover point, check `r` matches

## Weaknesses / Attack Angles
- **Weak/small curve order**: order is smooth → Pohlig-Hellman → ECDLP solvable
- **Invalid curve attack**: server doesn't validate received point is on curve → use low-order points on other curves, recover key mod small primes → CRT
- **ECDSA nonce reuse**: same `k` in two signatures → `k = (h1-h2)(s1-s2)⁻¹ mod n`, then `d = (sk - h)r⁻¹ mod n`
- **ECDSA biased nonce**: few bits of `k` known → lattice attack (HNP)
- **MOV attack**: curve is supersingular → pairing reduces ECDLP to DLP in finite field
- **Anomalous curve** (trace-of-Frobenius = 1): ECDLP solvable in polynomial time (Smart's attack)
- **`a=0` / `b=0`** degenerate curves: may reduce to simpler group

## Tools
- `sage` — `EllipticCurve(GF(p), [a, b])`, `discrete_log`, `order()`
- `tinyec` (Python) — lightweight EC arithmetic for toy challenges
- `pycryptodome` — ECDSA sign/verify on standard curves

## Quick Snippet

```python
# --- ECDSA nonce reuse: recover private key ---
# Two signatures (r, s1), (r, s2) with same k, messages h1, h2
from Crypto.Hash import SHA256
import gmpy2

n  = ...   # curve order
h1 = int(SHA256.new(msg1).hexdigest(), 16) % n
h2 = int(SHA256.new(msg2).hexdigest(), 16) % n
r, s1, s2 = ..., ..., ...

k  = (h1 - h2) * int(gmpy2.invert(s1 - s2, n)) % n
d  = (s1 * k - h1) * int(gmpy2.invert(r, n)) % n
print(f"Private key: {d}")
print(d.to_bytes((d.bit_length()+7)//8, 'big'))

# --- SageMath: ECDLP on small/weak curve ---
# p = ...
# E = EllipticCurve(GF(p), [a, b])
# G = E(Gx, Gy)
# Q = E(Qx, Qy)
# k = discrete_log(Q, G, operation='+')
# print(k)

# --- Check curve order smoothness (Python) ---
from sympy.ntheory import factorint
order = ...   # curve order n
print(factorint(order))   # if all small → Pohlig-Hellman applicable

# --- Point arithmetic (tinyec) ---
from tinyec import registry
curve = registry.get_curve('secp256r1')
G = curve.g
k = 42
Q = k * G
print(Q.x, Q.y)
```

## Spot it in a challenge when...
- Curve parameters given explicitly (non-standard curve) → check order
- Two ECDSA signatures with identical `r` → nonce reuse
- Server accepts arbitrary points → invalid curve attack
- Curve order is very small or has only small prime factors

## References
- [Cryptohack ECC challenges](https://cryptohack.org/challenges/ecc/)
- [ECDSA nonce reuse (Sony PS3 story)](https://fahrplan.events.ccc.de/congress/2010/Fahrplan/events/4087.en.html)

## Related
- [[diffie-hellman]]
- [[rsa]]
