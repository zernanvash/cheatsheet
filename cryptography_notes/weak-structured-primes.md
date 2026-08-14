# Weak and Structured RSA Primes

RSA does not fail merely because a prime has a recognizable mathematical name. It fails when a factor of `n = p*q` is recoverable because it is too small, too close to the other factor, reused, drawn from a known list, generated with low entropy, or has attackable neighboring structure.

> 💡 **Core distinction:** a sufficiently large Mersenne prime is still prime. In CTFs, the weakness is usually that it is a published constant or belongs to a tiny, guessable family—not that “Mersenne” automatically means weak.

## Fast Triage Order

Given public `(n, e)`, try cheap, evidence-driven attacks before general factoring:

1. Trial division, perfect-power checks, and obvious patterns.
2. Known/book primes: Mersenne, Fermat, primorial, Fibonacci, repunit, past-CTF lists.
3. GCD against every other supplied modulus.
4. Fermat factorization for close `p` and `q`.
5. Pollard `p-1` and Williams `p+1` for smooth neighboring orders.
6. ROCA fingerprint detection.
7. ECM for a comparatively small factor.
8. QS/NFS only after structure-specific attacks fail.

Always validate a recovered factor:

```python
assert 1 < p < n
assert n % p == 0
q = n // p
assert p * q == n
```

## Mersenne Primes

A Mersenne number is `M_k = 2^k - 1`. If it is prime, `k` must be prime, but a prime exponent does not guarantee a Mersenne prime.

Recognize a recovered factor:

```python
from sympy import isprime

def mersenne_form(value: int):
    if value < 3:
        return None
    power = value + 1
    if power & (power - 1):
        return None
    exponent = power.bit_length() - 1
    return exponent if isprime(exponent) and isprime(value) else None

p = 2**127 - 1
print(mersenne_form(p))  # 127
```

Test whether an RSA modulus contains a factor from a bounded exponent list:

```python
from math import gcd

def find_mersenne_factor(n: int, exponents):
    for exponent in exponents:
        candidate = (1 << exponent) - 1
        factor = gcd(n, candidate)
        if 1 < factor < n:
            return exponent, factor, n // factor
    return None

ctf_exponents = [31, 61, 89, 107, 127, 521, 607, 1279, 2203, 2281]
result = find_mersenne_factor(n, ctf_exponents)
if result:
    exponent, p, q = result
    assert p * q == n
    print(f"M_{exponent} factor:", p)
```

This is effective when a clue bounds `k`, a factor was copied from a published table, or the challenge mentions Mersenne, Lucas-Lehmer, or perfect numbers. It is not a general factoring method for random RSA moduli.

## Fermat Primes and “Book Primes”

A Fermat number is `F_k = 2^(2^k) + 1`. Only a tiny set of small Fermat numbers are known primes, so using one as an RSA factor makes the candidate list guessable.

```python
from math import gcd

def find_fermat_factor(n: int, max_k=12):
    for k in range(max_k + 1):
        candidate = (1 << (1 << k)) + 1
        factor = gcd(n, candidate)
        if 1 < factor < n:
            return k, factor, n // factor
    return None
```

Other CTF novelty families:

- primorials `2*3*5*...*p`, often adjusted by `±1` or a small constant;
- Fibonacci or Lucas numbers;
- `2^k ± small_value`;
- repunits `(10^k - 1)/9` and repeated-digit/palindromic primes;
- constants from standards, textbooks, source code, previous CTFs, or blog posts;
- consecutive `nextprime()` outputs around a memorable constant.

Test a hypothesis with GCD rather than trying to prove the candidate equals a factor first:

```python
from math import gcd
from sympy import primerange

running = 1
for prime in primerange(2, 200):
    running *= prime
    for candidate in (running - 1, running + 1):
        factor = gcd(n, candidate)
        if 1 < factor < n:
            print("primorial-style factor:", factor, n // factor)
```

## Close Primes: Fermat Factorization

When `p` and `q` are close, `n = a^2 - b^2 = (a-b)(a+b)`.

```python
from math import isqrt

def fermat_factor(n: int, max_steps=1_000_000):
    if n % 2 == 0:
        return 2, n // 2
    a = isqrt(n)
    if a * a < n:
        a += 1
    for _ in range(max_steps):
        b2 = a * a - n
        b = isqrt(b2)
        if b * b == b2:
            p, q = a - b, a + b
            if p * q == n:
                return p, q
        a += 1
    return None
```

Clues include “twins,” “neighbors,” “almost equal,” or source code such as `q = nextprime(p + small_delta)`.

## Shared or Reused Primes

Two moduli sharing one prime are broken by a single GCD:

```python
from itertools import combinations
from math import gcd

def shared_factors(moduli):
    for (i, left), (j, right) in combinations(enumerate(moduli), 2):
        factor = gcd(left, right)
        if 1 < factor < min(left, right):
            yield i, j, factor
```

For very large key collections, use a product-tree batch-GCD implementation instead of pairwise `O(k^2)` comparisons.

## Smooth `p-1` and `p+1`

- Pollard `p-1` works well when every prime factor of `p-1` is below a manageable bound.
- Williams `p+1` targets related structure in `p+1`.
- ECM is useful when one RSA factor is comparatively small; it is not simply another `p-1` test.

```python
from sympy.ntheory.factor_ import pollard_pm1

factor = pollard_pm1(n, B=100_000)
if factor not in (None, 1, n):
    assert n % factor == 0
    print(factor, n // factor)
```

If `p` is already known, inspect why the method succeeded:

```python
from sympy import factorint

print("p - 1:", factorint(p - 1))
print("p + 1:", factorint(p + 1))
```

Failure at one bound does not prove safety. Increase bounds deliberately and stop when the expected work no longer fits the challenge.

## Small or Unbalanced Factors

A modulus can have the expected total bit length yet be weak because one factor is far smaller than the other.

```python
from sympy import factorint

# Bounded trial division; this may return an incomplete factorization.
print(factorint(n, limit=1_000_000))
```

Sage/GMP-ECM:

```python
from sage.all import Integer

n = Integer(n)
print(n.factor(algorithm="ecm"))
```

```bash
echo "$N" | ecm 100000
```

## Biased or Predictable Prime Generation

Prime outputs may pass primality tests and still be weak because of:

- too few random seed bits;
- repeated PRNG state after reboot, VM cloning, or device resets;
- timestamp/PID-derived seeds;
- fixed or leaked high/low bits;
- deterministic generation from a small password space;
- vendor-specific generation patterns such as ROCA-affected Infineon RSALib.

ROCA can be detected from a public key without factoring it:

```bash
python -m pip install roca-detect
roca-detect key.pem
roca-detect certificate.pem
```

A fingerprint identifies an applicable weakness; it is not proof that you recovered the private key.

## Bad Primality Testing

A supposedly prime `p` may actually be composite because a generator used one Fermat test, too few Miller-Rabin bases, incorrect code, or attacker-controlled candidates.

```python
from sympy import isprime

assert isprime(p)
assert isprime(q)
assert p != q
assert p * q == n
```

Use maintained cryptographic libraries for production key generation. These helpers are for CTF analysis and validation.

## Strong and Safe Primes Are Not a Cure-All

- A safe prime is `p = 2q + 1` with prime `q`.
- `q` is then a Sophie Germain prime.
- A traditional “strong prime” has large prime factors in both `p-1` and `p+1`.

These properties do not repair reused primes, close factors, weak randomness, leaked bits, an undersized factor, a small private exponent, or broken padding. Modern RSA depends on adequate size, independent unpredictable generation, correct primality testing, and safe padding—not on a famous prime name.

## Tool Selection

| Tool | Best use |
| --- | --- |
| RsaCtfTool | Automated Fermat, Pollard, ROCA, novelty-prime, shared-factor, FactorDB, and non-factor attack triage |
| SymPy | `gcd`, `factorint`, `pollard_pm1`, perfect powers, primality testing, and scripts |
| SageMath | PARI/FLINT/GMP-ECM integration, lattices, finite fields, and custom algebra |
| GMP-ECM | Comparatively small factors plus P-1/P+1 modes |
| YAFU | Automated factorization pipeline and method selection |
| msieve | Quadratic-sieve and NFS-oriented workflows |
| FactorDB | Check whether a CTF modulus is already known; verify every result locally |
| `roca-detect` | Detect affected public keys and certificates |

RsaCtfTool quick start:

```bash
RsaCtfTool --publickey key.pem --private
RsaCtfTool --publickey key.pem --attack fermat
RsaCtfTool --publickey "*.pem" --private
RsaCtfTool --help
```

Attack identifiers can change; use `--help` from the installed version rather than guessing a name.

## Compact Triage Script

```python
from math import gcd
from sympy import perfect_power
from sympy.ntheory.factor_ import pollard_pm1

def triage_modulus(n: int, other_moduli=()):
    findings = []
    if n <= 1:
        return ["invalid modulus"]
    if n % 2 == 0:
        findings.append(("even", 2, n // 2))
    if perfect_power(n):
        findings.append(("perfect power", perfect_power(n)))
    for other in other_moduli:
        factor = gcd(n, other)
        if 1 < factor < n:
            findings.append(("shared factor", factor, n // factor))
    close = fermat_factor(n, 100_000)
    if close:
        findings.append(("close factors", close))
    factor = pollard_pm1(n, B=100_000)
    if factor not in (None, 1, n):
        findings.append(("smooth p-1", factor, n // factor))
    special = find_mersenne_factor(n, [31, 61, 89, 107, 127, 521, 607, 1279])
    if special:
        findings.append(("known Mersenne factor", special))
    return findings
```

## Evidence Checklist

- Record `n`, `e`, bit length, and source.
- State why each family or attack is being tested.
- Distinguish a fingerprint from a recovered factor.
- Verify `p*q == n` and primality of both factors.
- Reconstruct `d` and test an RSA round trip.
- Validate decrypted padding or known plaintext structure.
- Never call a key weak merely because a prime has a special name.

## References

- [RsaCtfTool attack inventory](https://github.com/RsaCtfTool/RsaCtfTool)
- [SymPy number theory](https://docs.sympy.org/latest/modules/ntheory.html)
- [SageMath integer factorization tutorial](https://doc.sagemath.org/html/en/thematic_tutorials/explicit_methods_in_number_theory/integer_factorization.html)
- [SageMath GMP-ECM interface](https://doc.sagemath.org/html/en/reference/interfaces/sage/interfaces/ecm.html)
- [CRoCS RSA key-bias and ROCA tools](https://crocs.fi.muni.cz/public/papers/rsabias)

