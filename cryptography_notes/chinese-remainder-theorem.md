---
tags: [ctf, crypto, rsa, math]
status: reference
---

# Chinese Remainder Theorem (CRT)

## Summary
Given a system of congruences `x ≡ aᵢ (mod nᵢ)` where all `nᵢ` are pairwise coprime, CRT guarantees a unique solution `x` mod `N` (where `N = n₁ × n₂ × … × nₖ`). In CTFs: most often weaponised against RSA (small `e`, multiple ciphertexts) or for modular reconstruction.

## How it works
- Unique solution: `x = Σ (aᵢ × Mᵢ × Mᵢ⁻¹) mod N`
  - `Mᵢ = N / nᵢ`
  - `Mᵢ⁻¹ = modular inverse of Mᵢ mod nᵢ`
- Pairwise coprime condition: `gcd(nᵢ, nⱼ) = 1` for all `i ≠ j`

## Weaknesses / Attack Angles
- **Håstad's Broadcast Attack**: same message `m` sent to `e` recipients, each with different modulus → CRT recovers `mᵉ mod N`, then take `e`-th integer root
- **Partial key exposure**: combine leaks from multiple moduli to reconstruct a full key or plaintext
- **Low `e` RSA**: if `e=3` and same `m` used 3× → `m³` recoverable, `m = cbrt(m³)` in integers

## Tools
- `sympy.ntheory.modular.crt` — pure-Python CRT solver
- `gmpy2.iroot(n, e)` — integer `e`-th root (for Håstad's final step)
- `pycryptodome` — RSA primitives

## Quick Snippet

```python
from sympy.ntheory.modular import crt
from gmpy2 import iroot

# --- Generic CRT ---
# remainders: [a1, a2, a3], moduli: [n1, n2, n3] (pairwise coprime)
remainders = [2, 3, 2]
moduli     = [3, 5, 7]
M, x = crt(moduli, remainders)   # x is solution, M is product of moduli
print(x % M)                      # unique solution mod M

# --- Manual CRT (no sympy) ---
def manual_crt(remainders, moduli):
    N = 1
    for m in moduli: N *= m
    x = 0
    for a, m in zip(remainders, moduli):
        Mi = N // m
        Mi_inv = pow(Mi, -1, m)   # Python 3.8+ built-in modular inverse
        x += a * Mi * Mi_inv
    return x % N

# --- Håstad's Broadcast Attack (e=3, three ciphertexts) ---
# c1 = m^3 mod n1,  c2 = m^3 mod n2,  c3 = m^3 mod n3
c = [c1, c2, c3]
n = [n1, n2, n3]
m_cubed = manual_crt(c, n)        # recover m^3 as an integer
m, exact = iroot(m_cubed, 3)      # cube root in integers
assert exact                       # if False: padding/salt was used
print(m.to_bytes((m.bit_length()+7)//8, 'big'))
```

## Spot it in a challenge when...
- Multiple RSA public keys with the **same small `e`** (e=3, e=5…)
- Challenge gives several `(c, n)` pairs for "the same message"
- Problem asks to reconstruct `x` from residues modulo different primes
- Hint mentions "broadcast encryption" or "Håstad"

## References
- [GeeksforGeeks — Chinese Remainder Theorem](https://www.geeksforgeeks.org/maths/chinese-remainder-theorem/)
- [CryptoHack — RSA Challenges (Broadcast)](https://cryptohack.org/challenges/rsa/)

## Related
- [[rsa]]
