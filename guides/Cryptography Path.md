# Cryptography Path

Workflow for CTF/lab cryptography, encodings, hashes, weak keys, and custom ciphers. First identify whether the task is encoding, encryption, hashing, or a broken implementation.

## 1. Triage

```bash
file data
strings -n 8 data
xxd data | head
wc -c data
```

Ask:

- Is it an encoding, not encryption?
- Is there a known prefix such as `flag{`, `picoCTF{`, or `H4G{`?
- Are there files named `public.pem`, `private.pem`, `id_rsa`, `cipher.txt`, `output.txt`, or `encrypt.py`?
- Is the ciphertext hex, Base64, decimal bytes, binary, Morse, or raw bytes?
- Is the challenge giving source code?

## 2. Linux CLI Tools

### Encodings

```bash
echo 'SGVsbG8=' | base64 -d
echo '666c6167' | xxd -r -p
printf '%b\n' '\\x66\\x6c\\x61\\x67'
```

ROT13:

```bash
echo 'synt' | tr 'A-Za-z' 'N-ZA-Mn-za-m'
```

Hashes:

```bash
hashid hash.txt
john hash.txt --wordlist=/usr/share/wordlists/rockyou.txt
hashcat -m MODE hash.txt rockyou.txt
```

Archives:

```bash
zip2john file.zip > zip.hash
rar2john file.rar > rar.hash
7z2john file.7z > 7z.hash
john zip.hash --wordlist=/usr/share/wordlists/rockyou.txt
```

### OpenSSL

Inspect keys:

```bash
openssl rsa -in private.pem -check -noout
openssl rsa -in private.pem -pubout
openssl x509 -in cert.pem -text -noout
```

RSA decrypt in older labs:

```bash
openssl rsautl -decrypt -inkey private.pem -in pass.enc
```

Symmetric decrypt examples:

```bash
openssl enc -d -aes-256-cbc -in cipher.bin -out plain.txt -k password
openssl enc -d -aes-256-cbc -pbkdf2 -in cipher.bin -out plain.txt -pass pass:password
```

## 3. Python Script Tools

### Bytes And Encoding Skeleton

```python
import base64

data = "666c6167"
print(bytes.fromhex(data))

b64 = "ZmxhZw=="
print(base64.b64decode(b64))
```

### XOR

```python
def xor_key(data, key):
    key = key if isinstance(key, bytes) else key.encode()
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))

ct = bytes.fromhex("2b272e2e2d")
for k in range(256):
    pt = bytes(b ^ k for b in ct)
    if all(32 <= c < 127 for c in pt):
        print(k, pt)
```

Known plaintext:

```python
ct = bytes.fromhex("0011223344")
known = b"flag{"
print(bytes(c ^ p for c, p in zip(ct, known)).hex())
```

### Caesar / ROT

```python
import string

alpha = string.ascii_lowercase
text = "uryyb"
for shift in range(26):
    out = "".join(alpha[(alpha.index(c) - shift) % 26] if c in alpha else c for c in text)
    print(shift, out)
```

### RSA Basics

```python
from Crypto.Util.number import long_to_bytes, inverse

n = 0
e = 65537
c = 0
p = 0
q = 0

phi = (p - 1) * (q - 1)
d = inverse(e, phi)
m = pow(c, d, n)
print(long_to_bytes(m))
```

### AES With PyCryptodome

```python
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

key = bytes.fromhex("00" * 16)
iv = bytes.fromhex("00" * 16)
ct = bytes.fromhex("00")

cipher = AES.new(key, AES.MODE_CBC, iv)
print(unpad(cipher.decrypt(ct), 16))
```

### Hash Brute Force Pattern

```python
import hashlib

target = "5f4dcc3b5aa765d61d8327deb882cf99"
with open("wordlist.txt", "rb") as f:
    for word in f:
        word = word.strip()
        if hashlib.md5(word).hexdigest() == target:
            print(word.decode(errors="ignore"))
            break
```

## 4. Web Tools

Use web tools for CTF data only, not sensitive real-world secrets.

- CyberChef: encoding chains, XOR, AES, RSA helpers, magic, entropy, decompression.
- dCode: Caesar, Vigenere, substitution, Bacon, Morse, rail fence, affine.
- FactorDB: small/known RSA modulus factorization.
- CrackStation: common unsalted hash lookup.
- jwt.io: JWT structure inspection; crack weak secrets locally.
- RsaCtfTool: local tool, useful for weak RSA attacks.

## 5. Decision Branches

### Encoding Chain

Signs: printable alphabet, padding `=`, hex-only, binary groups, Morse dots/dashes, decimal byte lists.

1. Decode one layer.
2. Run `file` or inspect output.
3. Repeat until plaintext or a new file type appears.
4. Use CyberChef when the chain is uncertain.

### Classical Cipher

Signs: alphabetic ciphertext, preserved spaces, challenge title hints, frequency patterns.

1. Try ROT/Caesar.
2. Try Vigenere if a key hint exists.
3. Try substitution with frequency tools.
4. Use known flag prefix as crib.

### XOR Or Repeating-Key XOR

Signs: hex bytes, known plaintext prefix, repeated patterns, source code using `^`.

1. Try single-byte XOR brute force.
2. Use known plaintext to recover keystream.
3. Check repeating key length.
4. Reconstruct plaintext with Python.

### RSA

Signs: `n`, `e`, `c`, PEM keys, `public.pem`, small exponent, multiple moduli.

1. Parse public key or given integers.
2. Check if `n` factors in FactorDB or with local tools.
3. Check common weaknesses: small `e`, shared prime, no padding, close primes.
4. Decrypt with Python after recovering `p` and `q`.

### Hashes

Signs: fixed-length hex/base64 strings, `$id$salt$hash`, `/etc/shadow`, archive hash output.

1. Identify hash type.
2. Prefer offline cracking with John/Hashcat.
3. Use challenge context to build custom wordlists.
4. Treat hashes as one-way unless the challenge is weak/common lookup.

### Custom Source Code

Signs: `encrypt.py`, `output.txt`, custom math, repeated XOR, shuffling, PRNG.

1. Read encryption code before guessing.
2. Identify reversible operations.
3. Reverse operations in opposite order.
4. Use known plaintext and small search spaces.
5. Use Z3 for constraints when direct reversal is awkward.

## 6. Study Use Cases

- [Cryptography examples](../references/Challenge%20Use%20Cases.md#cryptography)
- [REV Python Toolkit](../tools/REV%20Python%20Toolkit.md)
- [Password Attacks](../tools/Password%20Attacks.md)
