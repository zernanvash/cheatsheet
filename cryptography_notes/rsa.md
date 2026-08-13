---
tags: [ctf, crypto, rsa]
status: reference
---

# RSA

## Summary
- Textbook RSA: `c = m^e mod n`; decrypt with `m = c^d mod n` where `ed ≡ 1 mod λ(n)`.
- CTF RSA is usually a **parameter/reuse/oracle bug**, not a direct break of sound RSA-OAEP with a strong key.
- First triage: inventory every `n, e, c`, key size, reused values, leaks, and any decrypt/sign endpoint.

## How it works
- Keygen: primes `p,q`; `n=pq`; `λ(n)=lcm(p-1,q-1)`; `d=e⁻¹ mod λ(n)`.
- Encode bytes as integer: `m = int.from_bytes(msg, "big")`; require `0 ≤ m < n`.
- Public key: `(n,e)`; private information: `d` or enough data to recover `p,q`.
- Given factors: compute `d`, then `m = c^d mod n`; decode with `long_to_bytes(m)`.
- Real schemes add padding: OAEP for encryption, PSS for signatures. Many CTFs deliberately use raw/textbook RSA.

## Weaknesses / Attack Angles

| Attack | CTF condition / clue | Recovery idea |
|---|---|---|
| **Direct root / no wrap** | small `e`; `m^e < n`; one ciphertext | exact integer `e`-th root of `c` |
| **Håstad broadcast** | same unpadded `m`, same small `e`, at least `e` pairwise-coprime moduli | CRT the ciphertexts, then exact `e`-th root |
| **Common modulus** | same `n,m`; different coprime `e₁,e₂` | Bézout: `e₁a+e₂b=1`, so `m=c₁^a c₂^b mod n` |
| **Shared prime** | many public keys; two moduli reuse one prime | `p = gcd(n₁,n₂)`; batch-GCD all pairs/products |
| **Known/leaked factor** | `p`, `q`, `φ(n)`, `p+q`, or a factor relation is leaked | recover factors algebraically, then compute `d` |
| **Fermat factorization** | `p≈q`; modulus generated from nearby primes | write `n=a²-b²=(a-b)(a+b)` |
| **Pollard p−1** | one prime has smooth `p−1` | find `gcd(a^M−1,n)` for smooth exponent `M` |
| **Weak/small modulus** | short `n`, repeated challenge prime, suspicious generator | FactorDB, trial division, ECM, YAFU/msieve |
| **Wiener** | unusually small private exponent, roughly `d < n^(1/4)/3` | continued-fraction convergents of `e/n` |
| **Boneh–Durfee** | `d` somewhat larger than Wiener's range, roughly `d < n^0.292` | lattice attack; Sage implementation |
| **Partial prime leak** | high/low bits of `p` or `q`; `p = prefix+x` with small `x` | Coppersmith small roots in Sage |
| **Franklin–Reiter** | same `(n,e)`; `m₂ = a·m₁+b`; small `e` | polynomial GCD over `Z/nZ` |
| **Parity/LSB oracle** | endpoint reveals whether decrypted plaintext is odd/even | multiply by `2^e`; halve interval each query |
| **Bleichenbacher oracle** | PKCS#1 v1.5 endpoint distinguishes valid `00 02 ... 00` padding | adaptive chosen-ciphertext interval narrowing |
| **Faulty CRT signature** | correct and glitched signatures for the same message | `gcd(s_good-s_faulty,n)` reveals a prime |
| **Low-`e` signature forgery** | lax PKCS#1 v1.5 verification; `e=3` | craft a cube whose decoded prefix passes validation |
| **ROCA / structured primes** | vulnerable Infineon-generated public key | detect structure, then use specialist factorization |

- Preconditions matter: Håstad needs the **same unpadded message**; common modulus normally needs `gcd(e₁,e₂)=1` and invertible ciphertexts.
- If a negative Bézout exponent needs `c⁻¹ mod n` but `gcd(c,n)≠1`, that GCD may already reveal a factor.
- OAEP defeats the deterministic reuse/root attacks when correctly implemented; PKCS#1 v1.5 becomes dangerous when validity leaks.

## Tools
- `RsaCtfTool` — automated triage/factoring/known attacks: `python RsaCtfTool.py --publickey key.pem --attack all`
- `gmpy2` — `iroot`, `isqrt`, `invert`, `gcd`, big integers
- `pycryptodome` — `long_to_bytes`, key parsing/construction, OAEP/PSS primitives
- `FactorDB`, `yafu`, `msieve`, `cado-nfs` — known or offline factorization
- `SageMath` — polynomial rings, Franklin–Reiter, Coppersmith, lattice attacks
- `openssl pkey -pubin -in public.pem -text -noout` — inspect PEM public parameters

## Quick Snippet

```python
from itertools import combinations
from math import gcd, isqrt, lcm
from Crypto.Util.number import inverse, long_to_bytes
import gmpy2

def decode(m):
    return long_to_bytes(int(m))

def decrypt_from_factors(n, e, c, p, q):
    assert p * q == n
    d = inverse(e, lcm(p - 1, q - 1))
    return decode(pow(c, d, n))

# 1) Small plaintext / low e: succeeds only when c is an exact e-th power.
def direct_root(c, e):
    m, exact = gmpy2.iroot(c, e)
    return decode(m) if exact else None

# 2) Håstad: provide >= e encryptions of the same raw message.
def crt(items):                         # items = [(c, n), ...]
    N = 1
    for _, n in items:
        N *= n
    x = sum(c * (N // n) * inverse(N // n, n) for c, n in items) % N
    return x, N

def hastad(items, e):
    assert len(items) >= e
    x, _ = crt(items[:e])
    m, exact = gmpy2.iroot(x, e)
    return decode(m) if exact else None

# 3) Common modulus: negative exponents mean modular inverses.
def egcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x, y = egcd(b, a % b)
    return g, y, x - (a // b) * y

def signed_pow(c, k, n):
    return pow(c, k, n) if k >= 0 else pow(inverse(c, n), -k, n)

def common_modulus(n, e1, c1, e2, c2):
    g, a, b = egcd(e1, e2)
    assert g == 1
    return decode(signed_pow(c1, a, n) * signed_pow(c2, b, n) % n)

# 4) Shared-prime scan across supplied moduli.
def shared_primes(moduli):
    hits = []
    for (i, n1), (j, n2) in combinations(enumerate(moduli), 2):
        p = gcd(n1, n2)
        if 1 < p < min(n1, n2):
            hits.append((i, j, p))
    return hits

# 5) Fermat: fast only when p and q are close.
def fermat(n, max_steps=1_000_000):
    a = isqrt(n)
    if a * a < n:
        a += 1
    for _ in range(max_steps):
        b2 = a * a - n
        b = isqrt(b2)
        if b * b == b2:
            return a - b, a + b
        a += 1
    return None

# 6) Pollard p-1 stage 1: raise B when p-1 is less smoothly factored.
def pollard_p1(n, B=100_000):
    a = 2
    for j in range(2, B + 1):
        a = pow(a, j, n)
    p = gcd(a - 1, n)
    return (p, n // p) if 1 < p < n else None

# 7) Wiener: test continued-fraction convergents k/d of e/n.
def wiener(e, n):
    num, den = e, n
    p_nm2, p_nm1, q_nm2, q_nm1 = 0, 1, 1, 0
    while den:
        a, (num, den) = num // den, (den, num % den)
        k = a * p_nm1 + p_nm2
        d = a * q_nm1 + q_nm2
        p_nm2, p_nm1, q_nm2, q_nm1 = p_nm1, k, q_nm1, d
        if k == 0 or (e * d - 1) % k:
            continue
        phi = (e * d - 1) // k
        s = n - phi + 1
        disc = s * s - 4 * n
        if disc >= 0 and isqrt(disc) ** 2 == disc and (s + isqrt(disc)) % 2 == 0:
            return d
    return None
```

- **Parity-oracle PoC core:** start `[lo,hi]=[0,n]`; repeatedly set `c = c·2^e mod n`; if oracle says even set `hi=(lo+hi)/2`, else `lo=(lo+hi)/2`. Use exact rational bounds, not floats.
- **Franklin–Reiter PoC core (Sage):** build `f1=x^e-c1`, `f2=(a*x+b)^e-c2` over `PolynomialRing(Zmod(n))`; the monic polynomial GCD is normally `x-m`.
- **CRT-fault PoC:** for same-message signatures, try `p = gcd(s_good-s_faulty, n)`; if the challenge gives message representative `m`, also try `gcd(pow(s_faulty,e,n)-m,n)`.
- **Partial-bit PoC:** model the unknown portion as a small variable and call Sage `f.small_roots(X=2^unknown_bits, beta=...)`; bounds and polynomial depend on the leak.

## Spot it in a challenge when...
- Parse everything first: `n.bit_length()`, `e`, count of keys/ciphertexts, equality/reuse, and pairwise `gcd(nᵢ,nⱼ)`.
- `e=3` plus one `c` → exact root; `e=3` plus three same-message ciphertexts → Håstad.
- Same `n` with different exponents → common modulus; many `n` values → shared-prime scan.
- `p-q` hinted small → Fermat; prime-generation loop/smoothness hinted → Pollard `p−1`.
- `dp=d mod (p-1)`, `dq`, `qinv`, `φ(n)`, `p+q`, or high/low prime bits leaked → recover/factor algebraically or use Coppersmith.
- A server decrypts chosen ciphertexts, answers parity/padding validity, or signs chosen messages → oracle/signature attack, not factoring.
- PEM/DER files → inspect parameters; modulus below modern sizes or known challenge data → try FactorDB/RsaCtfTool early.
- `e=65537` is normal, not itself a weakness. A suspiciously small `d`, correlated primes, reuse, or leakage is the actual clue.

## References
- [RsaCtfTool](https://github.com/RsaCtfTool/RsaCtfTool)
- [CryptoHack RSA challenges](https://cryptohack.org/challenges/rsa/)
- [Boneh — Twenty Years of Attacks on RSA](https://crypto.stanford.edu/~dabo/pubs/papers/RSA-survey.pdf)

## Related
- [[chinese-remainder-theorem]]
- [[diffie-hellman]]
