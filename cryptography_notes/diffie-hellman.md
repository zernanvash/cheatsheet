---
tags: [ctf, crypto, diffie-hellman]
status: reference
---

# Diffie-Hellman (DH)

## Summary
Key exchange: both parties agree on shared secret without transmitting it. `g^(ab) mod p`. Broken in CTFs via weak parameters, small subgroup confinement, or when discrete log is tractable.

## How it works
- Public: prime `p`, generator `g`
- Alice: secret `a`, sends `A = g^a mod p`
- Bob: secret `b`, sends `B = g^b mod p`
- Shared secret: `s = B^a mod p = A^b mod p = g^(ab) mod p`

## Weaknesses / Attack Angles
- **Small `p`** (< ~1024 bit): discrete log with `pohlig-hellman` or `baby-step giant-step`
- **Pohlig-Hellman**: `p-1` is smooth (many small prime factors) → solve DL per factor, CRT
- **Small subgroup attack**: send `A = g^0 = 1` or a low-order element → shared secret is predictable
- **MITM**: no authentication → classic man-in-the-middle (intercept and replace both keys)
- **g=1 or g=p-1**: trivial shared secrets
- **Reused ephemeral key**: if `a` reused across sessions, correlation attacks apply
- **Invalid curve** (ECDH): send point not on curve → small-order group, recover key modularly

## Tools
- `sage` — `discrete_log(A, g, p-1, operation='mul')` or `GF(p)(A).log(g)`
- `sympy` — Pohlig-Hellman via `n_order`, `factorint`
- `openssl` — inspect live DH parameters

## Quick Snippet

```python
# --- Baby-step Giant-step (small discrete log) ---
# find x such that g^x ≡ A (mod p)
import math

def bsgs(g, A, p):
    n = math.isqrt(p) + 1
    # baby steps
    table = {pow(g, j, p): j for j in range(n)}
    gn = pow(pow(g, n, p), -1, p)   # g^(-n) mod p
    gamma = A
    for i in range(n):
        if gamma in table:
            return i * n + table[gamma]
        gamma = gamma * gn % p
    return None

g, A, p = ..., ..., ...
x = bsgs(g, A, p)
print(f"Discrete log: {x}")

# --- Pohlig-Hellman (SageMath, run in sage shell) ---
# p = ...
# g = Mod(g_val, p)
# A = Mod(A_val, p)
# print(discrete_log(A, g))

# --- Small subgroup: check order of received public key ---
from sympy.ntheory import factorint

def check_small_subgroup(B, p):
    order_candidates = factorint(p - 1)
    for factor in order_candidates:
        if pow(B, factor, p) == 1:
            print(f"Low-order element! order divides {factor}")

# --- Verify shared secret from known params ---
a, B, p = ..., ..., ...   # your secret, their public key, prime
shared = pow(B, a, p)
print(f"Shared secret: {shared}")
```

## Spot it in a challenge when...
- Challenge gives `p`, `g`, public keys `A`, `B`
- `p-1` factors are all small (run `factorint(p-1)`)
- `p` is less than 512 bits → BSGS or sage `discrete_log`
- Server accepts arbitrary `g` or `A` values → small subgroup test

## References
- [Cryptohack DH challenges](https://cryptohack.org/challenges/diffie-hellman/)
- [Pohlig-Hellman explanation](https://en.wikipedia.org/wiki/Pohlig%E2%80%93Hellman_algorithm)

## Related
- [[ecc]]
- [[chinese-remainder-theorem]]
