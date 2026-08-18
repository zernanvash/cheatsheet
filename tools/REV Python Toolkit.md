# REV Python Toolkit

Common Python helpers for reverse engineering, crackmes, binary parsing, byte conversion, XOR, crypto checks, symbolic solving, and angr workflows.

Reference analyzed: `hgbe02/Hackmyvm-HMVLabs-Temperance`, a set of Python solvers for HackMyVM Temperance levels using `pwntools`, encoding transforms, image parsing, hashing, OCR, QR decoding, ZIP parsing, HTTP parsing, and XOR.

> **Dedicated walkthrough:** [Temperance Challenge Solutions (levelx00-levelx32)](../rev_source/Temperance%20Challenge%20Solutions.md) documents every preserved level, recorded flag, reusable solver, dependency, and source correction.

## Core Libraries

- `bytes`, `bytearray`, `memoryview` - raw byte handling
- `struct` - pack/unpack binary integers and records
- `binascii` - hex/base64 helpers
- `base64` - Base64/Base32/Base85
- `hashlib` - MD5/SHA family
- `hmac` - keyed hashes
- `itertools` - permutations, combinations, product brute force
- `io` - in-memory file objects
- `zipfile` - ZIP parsing in memory
- `requests` - HTTP fetch/parse automation
- `PIL.Image` from `pillow` - image inspection
- `pytesseract` - OCR for image text
- `pyzbar` - QR/barcode decoding
- `Crypto.Cipher` from `pycryptodome` - AES/DES/ARC4/etc.
- `z3` - symbolic constraints
- `angr` - binary symbolic execution
- `capstone` - disassembly
- `keystone` - assembly
- `unicorn` - CPU emulation
- `lief` - PE/ELF/Mach-O parsing and patching
- `pefile` - PE parsing
- `elftools` - ELF parsing
- `pwntools` - packing, tubes, ELF helpers
- `sympy` - number theory, modular roots, CRT, factoring, and symbolic algebra
- `gmpy2` - fast GMP-backed large-integer arithmetic
- `sage` / SageMath - finite fields, polynomial rings, lattices, and integrated crypto mathematics

Install common stack:

```bash
python -m pip install pycryptodome z3-solver angr capstone keystone-engine unicorn lief pefile pyelftools pwntools
```

Add the common crypto-math helpers:

```bash
python -m pip install sympy gmpy2 pycryptodome
```

For image/OCR/QR challenge automation:

```bash
python -m pip install pillow pytesseract pyzbar requests
```

Tesseract OCR also needs the system package installed.

## Remote Challenge Template

Pattern from the Temperance solvers: connect, receive challenge, transform, send answer.

```python
from pwn import remote, log

HOST = "example.ctf.local"
PORT = 31337

s = remote(HOST, PORT)
banner = s.recv(1024)
log.info(banner.decode(errors="ignore"))

s.sendline(b"level-name")
challenge = s.recv(4096).strip()

answer = challenge  # replace with transform
s.sendline(answer if isinstance(answer, bytes) else str(answer).encode())

print(s.recv(4096).decode(errors="ignore"))
s.close()
```

Helpers for noisy services:

```python
line = s.recvline().strip()
s.recvuntil(b"Input: ")
s.sendline(b"answer")
```

## Bytes And Encoding

```python
data = b"ABC"
print(data.hex())
print(bytes.fromhex("414243"))
print(list(data))
print(data[::-1])
```

String to bytes:

```python
s = "hello"
b = s.encode()
print(b)
print(b.decode())
```

Integer conversions:

```python
n = 0x41424344
print(n.to_bytes(4, "big"))
print(n.to_bytes(4, "little"))
print(int.from_bytes(b"ABCD", "big"))
print(int.from_bytes(b"ABCD", "little"))
```

## struct Pack / Unpack

```python
import struct

buf = struct.pack("<I", 0x41424344)
print(buf)
print(struct.unpack("<I", buf)[0])
```

Formats:

- `<` little endian
- `>` big endian
- `B` uint8
- `H` uint16
- `I` uint32
- `Q` uint64

## Base Encodings

```python
import base64

raw = b"secret"
print(base64.b64encode(raw))
print(base64.b64decode(b"c2VjcmV0"))
print(base64.b32encode(raw))
print(base64.b85encode(raw))
```

Hex decode:

```python
print(bytes.fromhex("666c6167"))
print(b"flag".hex())
```

Decimal bytes to text:

```python
nums = "102 108 97 103".split()
print("".join(chr(int(n)) for n in nums))
```

## XOR Helpers

Single-byte XOR:

```python
def xor_byte(data, key):
    return bytes(b ^ key for b in data)

ct = bytes.fromhex("2b272e2e2d")
for k in range(256):
    pt = xor_byte(ct, k)
    if all(32 <= c < 127 for c in pt):
        print(k, pt)
```

Repeating-key XOR:

```python
def xor_key(data, key):
    key = key if isinstance(key, bytes) else key.encode()
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))

print(xor_key(b"hello", b"key"))
```

Repeating-key XOR for string challenges:

```python
def xor_text(text, key):
    return "".join(chr(ord(ch) ^ ord(key[i % len(key)])) for i, ch in enumerate(text))

print(xor_text("ciphertext", "HMV"))
```

Known-plaintext key recovery:

```python
ct = bytes.fromhex("0011223344")
known = b"flag{"
key_stream = bytes(c ^ p for c, p in zip(ct, known))
print(key_stream.hex())
```

## Common Challenge Snippet Templates

Use these as starting points when a decompiler shows familiar C patterns such as `srand()`, XOR loops, additive byte transforms, table shuffles, or checksum gates. Keep the candidate test function close to the decompiled logic, then print every plausible candidate and verify it against the original binary.

### C `rand()` / `srand()` Replay

Use when the binary seeds C PRNG with a fixed value, timestamp, username length, or visible integer and then compares generated values.

Linux/glibc `rand()` via `ctypes`:

```python
from ctypes import CDLL, c_uint

libc = CDLL("libc.so.6")

seed = 0x1337
libc.srand(c_uint(seed))

stream = [libc.rand() for _ in range(16)]
print(stream)
```

Windows/MSVCRT `rand()` via `ctypes`:

```python
from ctypes import CDLL, c_uint

msvcrt = CDLL("msvcrt.dll")

seed = 0x1337
msvcrt.srand(c_uint(seed))

stream = [msvcrt.rand() for _ in range(16)]
print(stream)
```

Timestamp seed brute force:

```python
from ctypes import CDLL, c_uint

libc = CDLL("libc.so.6")
target = [12345, 6789, 4242]  # values observed in the checker

for seed in range(1_700_000_000, 1_700_086_400):
    libc.srand(c_uint(seed))
    out = [libc.rand() for _ in range(len(target))]
    if out == target:
        print("seed", seed)
        break
```

When decompiled code uses `rand() % N`, replay the modulo exactly:

```python
libc.srand(c_uint(0x1337))
mask = bytes((libc.rand() % 256) for _ in range(32))
print(mask.hex())
```

### XOR Crackme Template

Use when the checker transforms each input byte with XOR and compares it with an expected byte array.

```python
expected = bytes.fromhex("2b 27 2e 2e 2d")
key = 0x42

plain = bytes(b ^ key for b in expected)
print(plain)
```

Brute-force one-byte XOR with printable scoring:

```python
def score(buf):
    common = b" etaoinshrdluETAOINSHRDLU{}_"
    return sum(c in common for c in buf) + sum(32 <= c < 127 for c in buf)

ct = bytes.fromhex("2b272e2e2d")

for key in range(256):
    pt = bytes(c ^ key for c in ct)
    if all(c in b"\n\r\t" or 32 <= c < 127 for c in pt):
        print(key, score(pt), pt)
```

Repeating XOR key recovery from known flag prefix:

```python
ct = bytes.fromhex("00112233445566778899")
known = b"flag{"

keystream = bytes(c ^ p for c, p in zip(ct, known))
print("known keystream:", keystream)

key_len = 5
key = bytearray(b"?" * key_len)
for i, k in enumerate(keystream):
    key[i % key_len] = k

print("partial key:", key)
```

### Add/Sub/Rotate Byte Transform

Use when each byte is adjusted by position, constant, or both.

```python
expected = [0x66, 0x6d, 0x63, 0x6a, 0x7f]

plain = bytes(((b - i) ^ 0x13) & 0xff for i, b in enumerate(expected))
print(plain)
```

Bit rotate helpers:

```python
def rol8(x, n):
    n &= 7
    return ((x << n) | (x >> (8 - n))) & 0xff

def ror8(x, n):
    n &= 7
    return ((x >> n) | (x << (8 - n))) & 0xff

expected = bytes.fromhex("8c 2d 4e")
plain = bytes(ror8(b, 3) ^ 0x55 for b in expected)
print(plain)
```

### Index Shuffle / Permutation Inversion

Use when the program compares `input[order[i]]` or writes bytes into a shuffled output buffer.

```python
order = [3, 0, 4, 1, 2]
shuffled = b"lohel"

plain = bytearray(len(shuffled))
for out_i, in_i in enumerate(order):
    plain[in_i] = shuffled[out_i]

print(bytes(plain))
```

### Checksum Gate Brute Force

Use when a small unknown suffix must satisfy sum, XOR, product, CRC-like, or modulo checks.

```python
import itertools
import string

prefix = "flag{"
suffix_len = 4
charset = string.ascii_lowercase + string.digits + "_"

def ok(s):
    data = s.encode()
    return sum(data) == 850 and (data[0] ^ data[-1]) == 0x12

for tup in itertools.product(charset, repeat=suffix_len):
    candidate = prefix + "".join(tup) + "}"
    if ok(candidate):
        print(candidate)
```

### Lookup Table Inversion

Use when each byte indexes a constant table and the output is compared to expected values.

```python
table = bytes.fromhex(
    "63 7c 77 7b f2 6b 6f c5 30 01 67 2b fe d7 ab 76"
)
expected = [0x7c, 0x2b, 0x63]

reverse = {}
for i, value in enumerate(table):
    reverse.setdefault(value, []).append(i)

for value in expected:
    print(value, reverse.get(value, []))
```

### Z3 For Small Arithmetic Checks

Use when constraints are easier to state than brute force.

```python
from z3 import Int, Solver, sat

a = Int("a")
b = Int("b")

s = Solver()
s.add(a >= 0, a <= 255)
s.add(b >= 0, b <= 255)
s.add(3 * a + 2 * b == 180)
s.add(a - b == 10)

if s.check() == sat:
    m = s.model()
    print(m[a].as_long(), m[b].as_long())
```

For fixed-width C behavior, use `BitVec`:

```python
from z3 import BitVec, Solver, sat

x = BitVec("x", 8)
s = Solver()
s.add(((x * 7) ^ 0x55) == 0x2a)

if s.check() == sat:
    print(s.model()[x].as_long())
```

## Modular Arithmetic And Crypto Math

Use this section when a challenge gives equations such as:

```text
x^2 ≡ a (mod p)
c ≡ m^e (mod n)
x ≡ r1 (mod p), x ≡ r2 (mod q)
```

The `% modulus` part changes the problem. A modular square root is not the ordinary real or integer square root: it asks for an integer `x` whose square leaves remainder `a` after division by the modulus.

### Dissecting `sympy.sqrt_mod`

```python
from sympy import isprime, sqrt_mod

a = 8479994658316772151941616510097127087554541274812435112009425778595495359700244470400642403747058566807127814165396640215844192327900454116257979487432016769329970767046735091249898678088061634796559556704959846424131820416048436501387617211770124292793308079214153179977624440438616958575058361193975686620046439877308339989295604537867493683872778843921771307305602776398786978353866231661453376056771972069776398999013769588936194859344941268223184197231368887060609212875507518936172060702209557124430477137421847130682601666968691651447236917018634902407704797328509461854842432015009878011354022108661461024768

p = 30531851861994333252675935111487950694414332763909083514133769861350960895076504687261369815735742549428789138300843082086550059082835141454526618160634109969195486322015775943030060449557090064811940139431735209185996454739163555910726493597222646855506445602953689527405362207926990442391705014604777038685880527537489845359101552442292804398472642356609304810680731556542002301547846635101455995732584071355903010856718680732337369128498655255277003643669031694516851390505923416710601212618443109844041514942401969629158975457079026906304328749039997262960301209158175920051890620947063936347307238412281568760161

print("probable prime modulus:", isprime(p))

root = sqrt_mod(a, p)
if root is None:
    print("No square root exists modulo p")
else:
    print("one root:", root)
    assert pow(root, 2, p) == a % p

    # For an odd prime, a nonzero root normally has the partner p - root.
    partner = (-root) % p
    assert pow(partner, 2, p) == a % p
    print("paired root:", partner)
```

What each part means:

- `a` is the residue whose square root you want.
- `p` is the modulus; the variable name suggests a prime, but always test or establish that assumption.
- `sqrt_mod(a, p)` solves `x**2 % p == a % p`; it does not compute `sqrt(a)`.
- The default call returns one root at most `p // 2`, but SymPy does not promise that it is the numerically smallest root.
- `None` means no modular square root exists.
- Never trust a solver result without checking `pow(root, 2, p) == a % p`.

Request every root only when the result set is expected to be small:

```python
from sympy import sqrt_mod

roots = sqrt_mod(a, p, all_roots=True)
print(roots)
assert all(pow(x, 2, p) == a % p for x in roots)
```

For a composite modulus, the number of roots can grow quickly. Iterate instead of constructing a large list:

```python
from sympy.ntheory.residue_ntheory import sqrt_mod_iter

for root in sqrt_mod_iter(a, p):
    assert pow(root, 2, p) == a % p
    print(root)
```

### First Checks Before Solving

```python
from math import gcd
from sympy import isprime, legendre_symbol

a %= p
print("bits:", p.bit_length())
print("gcd(a, p):", gcd(a, p))
print("prime modulus:", isprime(p))

if isprime(p) and p != 2 and gcd(a, p) == 1:
    symbol = legendre_symbol(a, p)
    print("Legendre symbol:", symbol)  # 1=root exists, -1=no root
```

The Legendre-symbol shortcut applies to an odd prime modulus. Do not use that conclusion blindly for composite moduli.

### Plain Python: The Core Operations

Modern Python already handles large integers and the three most common operations:

```python
from math import gcd, isqrt

g = gcd(a, p)
power = pow(a, 65537, p)       # efficient a**65537 mod p
inverse = pow(a, -1, p)        # raises ValueError when gcd(a, p) != 1
integer_root = isqrt(a)        # floor(sqrt(a)); not a modular root

assert (a * inverse) % p == 1
assert integer_root**2 <= a < (integer_root + 1)**2
```

When `p % 4 == 3` is prime, a square root has a short exponent formula:

```python
assert isprime(p) and p % 4 == 3
root = pow(a, (p + 1) // 4, p)
if pow(root, 2, p) != a % p:
    raise ValueError("a is not a quadratic residue modulo p")
```

That exponent shortcut is not a general replacement for Tonelli-Shanks or `sqrt_mod`.

### SymPy Number-Theory Toolkit

```python
from sympy import (
    discrete_log,
    factorint,
    integer_nthroot,
    isprime,
    mod_inverse,
    nextprime,
    nthroot_mod,
    primitive_root,
    quadratic_congruence,
)
from sympy.ntheory.modular import crt, solve_congruence

print(mod_inverse(17, 3120))
print(factorint(2**32 - 1))
print(integer_nthroot(27, 3))       # (3, True): ordinary exact integer root
print(nthroot_mod(8, 3, 13, True)) # modular cube roots
print(quadratic_congruence(1, 0, -10, 13))
print(primitive_root(17))
print(discrete_log(41, 15, 7))

x, modulus = crt([3, 5, 7], [2, 3, 2])
assert [x % m for m in (3, 5, 7)] == [2, 3, 2]

# Handles compatible non-coprime moduli too; returns None if inconsistent.
solution = solve_congruence((2, 3), (5, 6))
print(solution)
```

Keep these distinctions straight:

| Goal | Correct helper |
| --- | --- |
| Floor of the ordinary square root | `math.isqrt(n)` |
| Exact ordinary nth root | `sympy.integer_nthroot(n, k)` or `gmpy2.iroot(n, k)` |
| Square root modulo `m` | `sympy.sqrt_mod(a, m)` |
| Nth root modulo `m` | `sympy.nthroot_mod(a, k, m)` |
| Solve several congruences | `sympy.ntheory.modular.crt` / `solve_congruence` |
| Multiplicative inverse | `pow(a, -1, m)` / `sympy.mod_inverse` |

### SageMath: Best For Algebraic Structure

Sage is usually the cleanest choice when the challenge moves beyond integer helpers into finite fields, polynomial rings, elliptic curves, matrices, or lattices.

```python
p = 101
R = Zmod(p)
a = R(56)

roots = a.sqrt(all=True)
assert all(x**2 == a for x in roots)

inverse = R(17)^-1
assert R(17) * inverse == 1

F = GF(p)
PR.<x> = PolynomialRing(F)
print((x^3 + 2*x + 1).roots())
```

CRT and finite-field examples:

```python
result = crt([2, 3, 2], [3, 5, 7])
assert result % 3 == 2

F.<z> = GF(2^8)
print(z.multiplicative_order())
```

> 💡 **What to watch out for:** Sage uses `^` for exponentiation in Sage code, while ordinary Python uses `**`. In a normal `.py` file, `^` means bitwise XOR.

### `gmpy2`: Fast Large-Integer Primitives

Use `gmpy2` when the mathematics is already understood and the bottleneck is repeated big-integer work.

```python
import gmpy2

a = gmpy2.mpz(a)
p = gmpy2.mpz(p)

value = gmpy2.powmod(a, 65537, p)
inverse = gmpy2.invert(a, p)  # ZeroDivisionError if no inverse exists
root, exact = gmpy2.iroot(a, 2)

assert gmpy2.is_congruent(a * inverse, 1, p)
print(root, exact)  # ordinary integer root, not sqrt modulo p
```

For secret-dependent production operations, `gmpy2.powmod_sec` offers a constant-time modular exponentiation primitive under its documented input constraints. CTF solver scripts normally optimize for analysis speed, but do not mistake them for hardened cryptographic implementations.

### PyCryptodome: RSA And Byte Conversion Glue

PyCryptodome is not a general computer-algebra system. It is useful around RSA challenges for primes, inverses, key construction, and integer/byte conversion.

```python
from Crypto.Util.number import (
    bytes_to_long,
    getPrime,
    inverse,
    isPrime,
    long_to_bytes,
)

m = bytes_to_long(b"flag{example}")
block = long_to_bytes(m)
p = getPrime(1024)
d = inverse(65537, p - 1)

assert isPrime(p)
assert block == b"flag{example}"
```

Prefer native Python when it is equally clear:

```python
m = int.from_bytes(b"flag{example}", "big")
block = m.to_bytes((m.bit_length() + 7) // 8, "big")
```

### Which Library Should You Reach For?

| Situation | First choice | Why |
| --- | --- | --- |
| One inverse, GCD, modular power | Plain Python | Built in, exact, dependency-free |
| Modular roots, CRT, discrete logs, small factoring | SymPy | Direct number-theory API |
| Finite fields, polynomial systems, ECC, lattices | SageMath | Models the actual algebraic structures |
| Millions of large-integer operations | `gmpy2` | GMP-backed performance |
| RSA bytes, primes, and key objects | PyCryptodome | Practical crypto plumbing |
| Bit-vector constraints copied from a binary | Z3 | Models overflow and machine-width arithmetic |

### Validation-First CTF Workflow

1. Rewrite the challenge statement as an explicit congruence.
2. Record whether each modulus is known prime, composite, a prime power, or unknown.
3. Reduce inputs with `% modulus` and compute relevant GCDs.
4. Choose the narrowest solver that matches the mathematics.
5. Ask for all roots only when you understand how many may exist.
6. Verify every returned candidate by substituting it into the original equation.
7. Convert integers to bytes only after the math checks pass.
8. Check both endiannesses and preserve leading zero bytes when the protocol specifies a fixed block size.

Reusable verification pattern:

```python
def verified_modular_roots(a, modulus):
    from sympy import sqrt_mod

    roots = sqrt_mod(a, modulus, all_roots=True)
    if not roots:
        return []
    expected = a % modulus
    valid = [int(x) for x in roots if pow(int(x), 2, modulus) == expected]
    if len(valid) != len(roots):
        raise ValueError("solver returned an unverified candidate")
    return valid
```

### Common Mistakes

- Using `math.sqrt()` or floating point on 1,000-bit integers.
- Confusing `isqrt(a)` with a square root modulo `p`.
- Assuming a variable named `p` is prime without evidence.
- Keeping only one root when the plaintext could correspond to its paired root.
- Applying the `p % 4 == 3` shortcut to another prime class or a composite modulus.
- Calling CRT on non-coprime moduli without checking consistency.
- Treating `factorint()` as a magic RSA breaker; well-generated RSA moduli remain infeasible to factor.
- Converting a candidate to text before verifying the modular equation.
- Using Sage syntax such as `^` inside ordinary Python.

### Official References

- [SymPy number theory](https://docs.sympy.org/latest/modules/ntheory.html)
- [SageMath integers modulo n](https://doc.sagemath.org/html/en/reference/finite_rings/sage/rings/finite_rings/integer_mod.html)
- [SageMath finite rings](https://doc.sagemath.org/html/en/reference/finite_rings/sage/rings/finite_rings/integer_mod_ring.html)
- [gmpy2 integer functions](https://gmpy2.readthedocs.io/en/stable/mpz.html)
- [PyCryptodome `Crypto.Util.number`](https://pycryptodome.readthedocs.io/en/latest/src/util/util.html)

## Hashing

```python
import hashlib

data = b"password"
print(hashlib.md5(data).hexdigest())
print(hashlib.sha1(data).hexdigest())
print(hashlib.sha256(data).hexdigest())
```

Wordlist check:

```python
import hashlib

target = "5f4dcc3b5aa765d61d8327deb882cf99"
with open("wordlist.txt", "rb") as f:
    for line in f:
        word = line.strip()
        if hashlib.md5(word).hexdigest() == target:
            print(word.decode(errors="ignore"))
            break
```

Permutation brute force against an MD5:

```python
import hashlib
import itertools

target = "md5_here"
chars = "abc123"

for perm in itertools.permutations(chars):
    candidate = "".join(perm)
    if hashlib.md5(candidate.encode()).hexdigest() == target:
        print(candidate)
        break
```

Cartesian brute force for fixed charset/length:

```python
import itertools

charset = "abcdef012345"
for tup in itertools.product(charset, repeat=4):
    candidate = "".join(tup)
    # test candidate
```

## Morse

```python
MORSE = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.",
    "G": "--.", "H": "....", "I": "..", "J": ".---", "K": "-.-", "L": ".-..",
    "M": "--", "N": "-.", "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.",
    "S": "...", "T": "-", "U": "..-", "V": "...-", "W": ".--", "X": "-..-",
    "Y": "-.--", "Z": "--..", "0": "-----", "1": ".----", "2": "..---",
    "3": "...--", "4": "....-", "5": ".....", "6": "-....", "7": "--...",
    "8": "---..", "9": "----."
}

REV_MORSE = {v: k for k, v in MORSE.items()}
msg = ".-- ...- .-. --.."
print("".join(REV_MORSE[x] for x in msg.split()))
```

## AES With PyCryptodome

```python
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

key = b"A" * 16
iv = b"B" * 16
pt = b"message"

cipher = AES.new(key, AES.MODE_CBC, iv)
ct = cipher.encrypt(pad(pt, 16))

cipher = AES.new(key, AES.MODE_CBC, iv)
print(unpad(cipher.decrypt(ct), 16))
```

ECB check:

```python
blocks = [ct[i:i+16] for i in range(0, len(ct), 16)]
print(len(blocks) != len(set(blocks)))
```

## ROT And Caesar

```python
import codecs

print(codecs.decode("synt", "rot_13"))
```

Caesar brute force:

```python
import string

alpha = string.ascii_lowercase
text = "uryyb"
for shift in range(26):
    out = "".join(alpha[(alpha.index(c) - shift) % 26] if c in alpha else c for c in text)
    print(shift, out)
```

## Binary File Helpers

Read file:

```python
from pathlib import Path

data = Path("sample.bin").read_bytes()
print(len(data), data[:16].hex())
```

Patch bytes:

```python
from pathlib import Path

data = bytearray(Path("sample.bin").read_bytes())
data[0x100:0x104] = b"\x90\x90\x90\x90"
Path("patched.bin").write_bytes(data)
```

Find strings:

```python
import re
from pathlib import Path

data = Path("sample.bin").read_bytes()
for s in re.findall(rb"[ -~]{4,}", data):
    print(s.decode(errors="ignore"))
```

## In-Memory ZIP

Useful when a service sends a Base64 ZIP and expects the content of the first file.

```python
import base64
import io
import zipfile

blob = base64.b64decode(challenge)
zf = zipfile.ZipFile(io.BytesIO(blob))
name = zf.namelist()[0]
content = zf.read(name)
print(content.decode(errors="ignore"))
```

## Images From Base64

Open an image without writing it to disk:

```python
import base64
import io
from PIL import Image

blob = base64.b64decode(challenge)
img = Image.open(io.BytesIO(blob))
print(img.size)
print(img.mode)
```

Read pixels:

```python
pixels = img.load()
print(pixels[0, 0])

for x in range(img.width):
    r, g, b, *rest = pixels[x, 0]
    alpha = rest[0] if rest else None
```

Extract text from RGBA alpha values:

```python
out = []
for x in range(img.width):
    px = img.getpixel((x, 0))
    if len(px) == 4:
        out.append(chr(px[3]))
print("".join(out))
```

## OCR

```python
import base64
import io
from PIL import Image
import pytesseract

img = Image.open(io.BytesIO(base64.b64decode(challenge)))
text = pytesseract.image_to_string(img).strip()
print(text)
```

If OCR is noisy, preprocess:

```python
img = img.convert("L")
img = img.point(lambda p: 255 if p > 160 else 0)
```

## QR Decode

```python
import base64
import io
from PIL import Image
import pyzbar.pyzbar as pyzbar

img = Image.open(io.BytesIO(base64.b64decode(challenge)))
decoded = pyzbar.decode(img)
print("".join(d.data.decode() for d in decoded))
```

## HTTP Parsing Automation

Fetch a URL from a challenge and extract a field from `/etc/passwd` style content:

```python
import requests

url = challenge.decode().strip()
body = requests.get(url, timeout=10).text

for line in body.splitlines():
    parts = line.split(":")
    if len(parts) > 2 and parts[0] == "proxy":
        print(parts[2])
```

## Z3 Basics

```python
from z3 import *

x = Int("x")
y = Int("y")
s = Solver()
s.add(x + y == 10)
s.add(x > 0, y > 0)

if s.check() == sat:
    m = s.model()
    print(m[x], m[y])
```

Byte constraints:

```python
from z3 import *

chars = [BitVec(f"c{i}", 8) for i in range(4)]
s = Solver()
for c in chars:
    s.add(c >= 0x20, c <= 0x7e)
s.add(chars[0] ^ chars[1] == 0x10)
s.add(chars[2] + chars[3] == 150)

if s.check() == sat:
    m = s.model()
    print(bytes([m[c].as_long() for c in chars]))
```

## Linear And Matrix Solvers

Use when a checker computes repeated sums like `a0*flag[0] + a1*flag[1] + ... == target`, matrix products, or many modulo-byte equations.

Z3 modulo 256 system:

```python
from z3 import BitVec, Solver, sat

SIZE = 64
matrix = [...]  # row-major SIZE * SIZE coefficients
target = [...]  # SIZE target bytes

flag = [BitVec(f"flag_{i}", 8) for i in range(SIZE)]
s = Solver()

for c in flag:
    s.add(c >= 0x20, c <= 0x7e)

for row in range(SIZE):
    acc = 0
    for col in range(SIZE):
        acc += matrix[row * SIZE + col] * flag[col]
    s.add((acc & 0xff) == target[row])

if s.check() == sat:
    m = s.model()
    print(bytes(m[c].as_long() for c in flag))
```

Decode obfuscated constants before solving:

```python
def decode_byte(b):
    return (13 * ((~b) & 0xff) + 223) & 0xff

matrix = [decode_byte(b) for b in matrix_raw]
target = [decode_byte(b) for b in target_raw]
```

NumPy quick solve for ordinary linear systems:

```python
import numpy as np

A = np.array(coefficients, dtype=np.int64)
b = np.array(targets, dtype=np.int64)
x = np.linalg.lstsq(A, b, rcond=None)[0]
print(bytes(round(v) & 0xff for v in x))
```

Try `np.linalg.solve(A, b)` for square invertible systems and `np.linalg.pinv(A) @ b` when a pseudoinverse is useful.

## VM And State Machine Helpers

Use when a program has a dispatcher loop, custom opcodes, state tables, or many tiny state functions.

Trace record shape:

```python
trace = []

def log(pc, op, *args):
    trace.append((pc, op, args))

log(pc, "LOAD_INPUT", idx)
log(pc, "PUSH", value)
log(pc, "MUL")
log(pc, "STORE", addr)

for pc, op, args in trace:
    print(pc, op, args)
```

Translate trace comments into equations:

```python
rows = []
current = []

for line in open("operations.log", encoding="utf-8"):
    line = line.strip()
    if "Load from memory[" in line:
        current.append(("load", int(line.split("[")[1].split("]")[0])))
    elif "Push immediate" in line:
        current.append(("imm", int(line.rsplit(" ", 1)[1])))
    elif "Store to memory[" in line:
        rows.append(current)
        current = []
```

Graph/path validators:

```python
from collections import defaultdict

edges = defaultdict(list)
for src, dst, symbol in transitions:
    edges[src].append((dst, symbol))

path = []
used = set()

def dfs(node):
    if len(path) == TARGET_EDGE_COUNT:
        return True
    for nxt, sym in sorted(edges[node], key=lambda e: len(edges[e[0]])):
        key = (node, nxt, sym)
        if key in used:
            continue
        used.add(key)
        path.append(sym)
        if dfs(nxt):
            return True
        path.pop()
        used.remove(key)
    return False

dfs(0)
print(bytes(path))
```

## angr Skeleton

```python
import angr

project = angr.Project("./binary", auto_load_libs=False)
state = project.factory.entry_state()
simgr = project.factory.simulation_manager(state)

simgr.explore(find=0x401234, avoid=0x401000)

if simgr.found:
    found = simgr.found[0]
    print(found.posix.dumps(0))
```

Symbolic stdin:

```python
import angr
import claripy

project = angr.Project("./binary", auto_load_libs=False)
flag = claripy.BVS("flag", 8 * 32)
state = project.factory.full_init_state(stdin=flag)

for byte in flag.chop(8):
    state.solver.add(byte >= 0x20, byte <= 0x7e)

simgr = project.factory.simulation_manager(state)
simgr.explore(find=0x401234, avoid=0x401000)

if simgr.found:
    print(simgr.found[0].solver.eval(flag, cast_to=bytes))
```

## Capstone Disassembly

```python
from capstone import *

code = bytes.fromhex("554889e5")
md = Cs(CS_ARCH_X86, CS_MODE_64)
for insn in md.disasm(code, 0x1000):
    print(hex(insn.address), insn.mnemonic, insn.op_str)
```

## Keystone Assembly

```python
from keystone import *

ks = Ks(KS_ARCH_X86, KS_MODE_64)
encoding, count = ks.asm("xor eax, eax; ret")
print(bytes(encoding).hex())
```

## PE / ELF Quick Checks

PE:

```python
import pefile

pe = pefile.PE("sample.exe")
print(hex(pe.OPTIONAL_HEADER.ImageBase))
for section in pe.sections:
    print(section.Name, hex(section.VirtualAddress), hex(section.Misc_VirtualSize))
```

ELF:

```python
from elftools.elf.elffile import ELFFile

with open("sample", "rb") as f:
    elf = ELFFile(f)
    print(elf.header["e_machine"])
    for sec in elf.iter_sections():
        print(sec.name, hex(sec["sh_addr"]))
```

## pyc / PyInstaller

Common tools:

- `pyinstxtractor.py` - extract PyInstaller bundles
- `pyinstxtractor-ng` - newer PyInstaller extraction helper
- `uncompyle6`, `decompyle3`, or PyLingual - decompile Python bytecode when supported
- Pyarmor static unpackers - recover bytecode/disassembly from protected Python when safe and legal

Flow:

1. Identify with `file`.
2. Extract with PyInstaller extractor if bundled.
3. Match Python version.
4. Decompile `.pyc`.
5. Read constants with `strings` or `dis` when decompile fails.
6. Trust bytecode/disassembly over broken generated source.

Python `dis`:

```python
import dis

def check(x):
    return x[::-1] == "terces"

dis.dis(check)
```

Marshal bytecode key brute force:

```python
import dis
import marshal

blob = bytes.fromhex("...")

for key in range(256):
    try:
        code = marshal.loads(bytes(b ^ key for b in blob))
        print("key", key)
        dis.dis(code)
        break
    except (EOFError, TypeError, ValueError):
        pass
```

Pyarmor cleanup clues:

- ignore protector enter/exit wrapper markers
- replace readable assert/runtime helper calls with their underlying value
- split large disassembly into the function you care about first
- reconstruct loops and checks one basic block at a time

## Script And Payload Deobfuscation

Useful for shell, zsh, bash, plist, mobileconfig, and staged payload challenges.

```python
from html import unescape

script = open("document.wflow", encoding="utf-8", errors="ignore").read()
script = unescape(script)
print(script)
```

ROT/reverse/tr-like transforms:

```python
import codecs

text = "gkg.erqvibeC"
print(codecs.decode(text, "rot_13")[::-1])
```

Base64 and hex:

```python
import base64

print(base64.b64decode("c2VjcmV0"))
print(bytes.fromhex("68656c6c6f"))
```

When a script uses `${var:offset:length}`, `$0`, comments, filenames, or undefined variables, evaluate those expressions literally. Comments and script paths can be intentional key material.

## PBM / Bitmap Bit Extraction

Use when the program emits `P1`, `P2`, `P3`, or a simple visual grid.

```python
from pathlib import Path

text = Path("out.pbm").read_text()
parts = text.split(maxsplit=3)
width = int(parts[1])
body = "".join(ch for ch in parts[3] if ch in "01")
rows = [body[i:i+width] for i in range(0, len(body), width)]

for row in rows[:8]:
    print(row)
```

Recover a packed value once margins and bit order are known:

```python
groups = []
for row in rows:
    useful = row[1:6]          # adjust after mapping
    groups.append(useful[::-1])

bits = "".join(reversed(groups))
value = int(bits, 2)
print(value.to_bytes((value.bit_length() + 7) // 8, "big"))
```

## picoCTF REV Patterns

Integrated from `Cajac/picoCTF-Writeups`. These are common CTF reverse engineering branches, especially useful before reaching for heavier tools.

### First Triage Commands

```bash
file ./challenge
strings -n 8 ./challenge
chmod +x ./challenge
./challenge
objdump -d ./challenge | less
```

Branch quickly:

- obvious strings -> validate and submit
- register/address question -> use GDB
- Python source -> patch or reproduce checks
- Java/APK -> decompile with jadx
- WebAssembly -> use WABT tools
- sparse strings or UPX marker -> unpack first

### GDB Register And Memory Tasks

```bash
gdb ./challenge
layout asm
break *main
run
info registers
x/s 0xADDRESS
x/16xb 0xADDRESS
disassemble main
```

For picoCTF baby-step style tasks, set a breakpoint at the requested address, run to it, then inspect the named register or memory address. Convert decimal, hex, or ASCII exactly as requested by the prompt.

### Byte Transform Solver Skeleton

Use for XOR, addition/subtraction, index shuffles, and simple flag validation loops.

```python
def transform(data):
    out = bytearray()
    for i, b in enumerate(data):
        out.append((b ^ 0x42) & 0xff)
    return bytes(out)

candidate = bytes.fromhex("001122334455")
print(transform(candidate))
```

Index shuffle pattern:

```python
data = b"example_flag_order"
order = [3, 0, 1, 2]
print(bytes(data[i] for i in order))
```

Reverse a check that stores expected transformed bytes:

```python
expected = [0x20, 0x27, 0x23, 0x25]
plain = bytes(x ^ 0x42 for x in expected)
print(plain)
```

### Python Source And Bytecode

If `.py` is provided:

- read constants and comparison functions
- decode Base64/hex before executing unknown logic
- remove sleeps and failure exits in a local copy
- use `dis` when the check is hidden in bytecode-style logic

```python
import dis

def check(value):
    return value[::-1] == "terces"

dis.dis(check)
```

### Java, APK, And WebAssembly

Java/APK:

```bash
jadx-gui app.apk
```

Check `MainActivity`, resources, hardcoded strings, native library loading, and validation methods.

WebAssembly:

```bash
wasm2wat module.wasm -o module.wat
wasm-decompile module.wasm > module.c
strings -n 8 module.wasm
```

Search for exported check functions, memory offsets, expected byte arrays, and simple transforms.

### Packed Or Obfuscated Binaries

```bash
upx -d ./challenge
file ./challenge
strings -n 8 ./challenge
```

If unpacking fails, debug runtime behavior and search for decrypted strings after the program initializes.

## Useful External References

- Anti-debug reference: https://anti-debug.checkpoint.com/
- PyLingual: https://www.pylingual.io/
- Online x86 assembler: https://defuse.ca/online-x86-assembler.htm
- pyinstxtractor: https://github.com/extremecoders-re/pyinstxtractor
- decompyle builds: https://github.com/extremecoders-re/decompyle-builds
- Local x86 guide: [Guide to x86 Assembly](../references/Guide%20to%20x86%20Assembly.html)
- Local syscall table: [Linux x86_64 syscall table](../references/Linux%20System%20Call%20Table%20for%20x86%2064%20-%20Ryan%20A.%20Chapman.html)
- Local C reversing patterns: [C Reversing Cheat Sheet](C%20Reversing%20Cheat%20Sheet.md)
