# RsaCtfTool: Weak RSA Analysis Guide

RsaCtfTool is a multi-attack utility for CTF RSA problems. It tries known weaknesses in public keys, factors vulnerable moduli, reconstructs private keys, and decrypts ciphertext when the mathematics permits it.

> 💡 **What to watch out for:** RsaCtfTool does not "break RSA" in general. It succeeds when the challenge uses weak parameters, related keys, textbook RSA, reused primes, small exponents, close factors, or another recognizable construction flaw.

## Learning Goals

- Decide whether a challenge is suitable for RsaCtfTool.
- Turn `n` and `e` into a public key.
- Choose automatic or targeted attacks from evidence.
- Recover, inspect, and validate a private key.
- Decrypt raw CTF ciphertext without losing padding evidence.
- Recognize when to switch to SageMath, custom Python, YAFU, msieve, or CADO-NFS.

## 1. The RSA Model Being Attacked

Textbook RSA starts with two primes:

```text
n = p × q
φ(n) = (p − 1)(q − 1)
e × d ≡ 1 mod φ(n)
c ≡ m^e mod n
m ≡ c^d mod n
```

The public key contains `(n, e)`. The private key contains enough information to use `d`, usually including `p` and `q`. RsaCtfTool searches for shortcuts to that private information.

| Weakness | Evidence | Why it helps |
|---|---|---|
| Close primes | `p` and `q` were generated near each other | Fermat factorization finds the nearby square quickly |
| Shared prime | Multiple moduli have a common factor | `gcd(n1, n2)` reveals that prime immediately |
| Small private exponent | Unusually small `d` | Wiener's or Boneh-Durfee attack may recover `d` |
| Small public exponent | Often `e = 3`, related messages, or several recipients | Hastad/broadcast or direct-root conditions may recover `m` |
| Smooth `p − 1` or `p + 1` | Hints about smoothness or special prime generation | Pollard p−1 or Williams p+1 may factor `n` |
| Known factorization | The modulus has already been submitted | FactorDB returns `p` and `q` |
| Weak generator | ROCA or gimmicky/novelty primes | Structure reduces the search space |
| Partial secret | Bits or digits of `p`, `q`, or `d` leak | Lattice or partial-key attacks reconstruct the rest |

The upstream README states that the tool targets textbook RSA with a semiprime modulus and does not support multiprime RSA. Secure modern RSA with appropriate padding and no parameter weakness should not be recoverable.

## 2. Collect Evidence First

Inventory every supplied value and file:

```bash
file *.pem *.pub *.key *.enc *.bin 2>/dev/null
find . -maxdepth 2 -type f -printf '%p\n'
```

Look for:

- `public.pem`, `key.pub`, certificates, or SSH public keys;
- integers labelled `n`, `e`, and `c`;
- several public keys or ciphertexts;
- source code showing prime generation or padding;
- hints such as *close*, *broadcast*, *shared*, *smooth*, *small*, *partial*, or *ROCA*;
- ciphertext represented as raw bytes, hexadecimal, Base64, or a decimal integer.

Inspect a public key:

```bash
openssl pkey -pubin -in key.pub -text -noout
```

Extract a public key from a certificate:

```bash
openssl x509 -in certificate.pem -pubkey -noout > key.pub
openssl pkey -pubin -in key.pub -text -noout
```

> 💡 **What to watch out for:** Determine whether `ciphertext` is a raw encrypted byte string or a textual integer. `--decryptfile` expects ciphertext bytes. A decimal `c = ...` may need conversion or a different option shown by your installed `RsaCtfTool --help`.

## 3. Install in an Isolated Environment

Upstream currently requires Python 3.9 or newer. SageMath is optional but recommended because some lattice attacks depend on it.

### Python Virtual Environment

```bash
git clone https://github.com/RsaCtfTool/RsaCtfTool.git
cd RsaCtfTool
python3 -m venv venv
source venv/bin/activate
pip install -e .
RsaCtfTool --help
```

PowerShell:

```powershell
git clone https://github.com/RsaCtfTool/RsaCtfTool.git
Set-Location RsaCtfTool
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -e .
RsaCtfTool --help
```

### Docker

```bash
git clone https://github.com/RsaCtfTool/RsaCtfTool.git
cd RsaCtfTool
docker build -t rsactftool/rsactftool .
docker run --rm -it -v "$PWD:/data" rsactftool/rsactftool --help
```

Challenge files in the mounted directory appear under `/data`:

```bash
docker run --rm -it -v "$PWD:/data" rsactftool/rsactftool --publickey /data/key.pub --private
```

## 4. Inspect Before Attacking

Dump public parameters:

```bash
RsaCtfTool --dumpkey --key key.pub
```

Include CRT parameters for a private key:

```bash
RsaCtfTool --dumpkey --ext --key private.pem
```

Use the output to answer:

- Is this genuinely an RSA key?
- What are the modulus size, `n`, and `e`?
- Is `e` unusually small or huge?
- Does a recovered key contain plausible `p`, `q`, and `d` values?

## 5. Create a Public Key From `n` and `e`

CTFs often provide integers rather than PEM:

```bash
export RSA_N='7828374823761928712873'
export RSA_E='65537'
RsaCtfTool --createpub -n "$RSA_N" -e "$RSA_E" > key.pub
RsaCtfTool --dumpkey --key key.pub
```

Replace the demonstration modulus with the complete challenge value. The generated key becomes reusable input for later commands.

## 6. Automatic Private-Key Recovery

```bash
RsaCtfTool --publickey key.pub --private
```

Use automatic mode when one key is supplied and no strong attack hint exists. Record:

- the attack that reported success;
- recovered factors and key output;
- whether a network service such as FactorDB supplied the factors;
- elapsed time and missing optional dependencies.

Save PEM output when the installed version writes a clean key to standard output:

```bash
RsaCtfTool --publickey key.pub --private > recovered-private.pem
openssl pkey -in recovered-private.pem -check -text -noout
```

If logs are mixed with the key, retain only the complete `BEGIN ... PRIVATE KEY` through `END ... PRIVATE KEY` block.

## 7. Targeted Attacks

Attack identifiers can change. Confirm them first:

```bash
RsaCtfTool --help
```

### Wiener's Attack

```bash
RsaCtfTool --publickey key.pub --attack wiener --private
```

Wiener's attack uses continued fractions to recover a sufficiently small `d`. Failure only rejects this weakness; it does not prove the key secure.

### Fermat Factorization

Use Fermat when source or hints imply close primes. It searches for:

```text
n = a² − b² = (a − b)(a + b)
```

It is excellent for close factors and poor for securely generated, randomly separated primes. Confirm the installed Fermat attack identifier with `--help` before invoking it.

### FactorDB

```bash
RsaCtfTool --publickey key.pub --attack factordb --private
```

> 💡 **What to watch out for:** FactorDB is external. Do not send private, production, or engagement-sensitive moduli. For public CTF keys it is normally acceptable unless rules forbid external services.

Publishing recovered factors is a separate action:

```bash
RsaCtfTool --publickey "*.pub" --private --sendtofdb
```

Only use `--sendtofdb` deliberately.

### ECM

```bash
RsaCtfTool --publickey key.pub --ecmdigits 25 --private
```

ECM is useful when one factor is relatively small. `--ecmdigits` describes expected factor digits, not total key size.

### ROCA

```bash
RsaCtfTool --isroca --publickey "*.pub"
```

A positive check identifies vulnerable Infineon key structure. Recovery cost still depends on key size and available tooling.

### Broadcast and Shared-Key Cases

Hastad's broadcast attack needs the same plaintext encrypted with the same small `e` under several coprime moduli. One key/ciphertext is normally insufficient unless `m^e < n`, allowing an exact integer root.

Shared-prime attacks also require several keys:

```text
gcd(n1, n2) = p, where 1 < p < n1
```

Keep all related keys together:

```bash
RsaCtfTool --publickey "keys/*.pub" --private
```

Preserve which ciphertext belongs to which public key.

## 8. Decrypt Ciphertext

For a public key and raw ciphertext file:

```bash
RsaCtfTool --publickey key.pub --decryptfile ciphertext.bin
```

Inspect decrypted output as bytes:

```bash
file plaintext.bin
xxd plaintext.bin | head
strings -n 4 plaintext.bin
```

### Padding Changes the Interpretation

CTF textbook RSA often maps an integer directly to bytes. Real RSA normally uses OAEP or PKCS#1 v1.5 encryption padding. Recovering `d` does not guarantee readable raw output. Identify the padded block and use an operation matching its scheme.

> 💡 **What to watch out for:** Do not strip bytes until the output looks readable. Preserve the original decrypted block and identify its padding first.

## 9. Multiple-Key Workflow

Multiple keys can expose reused primes, broadcast conditions, ROCA keys, or one deliberately weak member:

```bash
mkdir -p keys ciphertexts
RsaCtfTool --publickey "keys/*.pub" --private
```

Use paired names:

```text
keys/alice.pub
keys/bob.pub
ciphertexts/alice.bin
ciphertexts/bob.bin
```

## 10. Convert an SSH RSA Public Key

```bash
RsaCtfTool --convert_idrsa_pub --publickey id_rsa.pub
```

This converts format; it does not recover a private key. Inspect the converted PEM before attacking it:

```bash
openssl pkey -pubin -in key.pub -text -noout
```

## 11. Read Failure Correctly

| Result | Interpretation | Next action |
|---|---|---|
| No attack succeeds | No enabled weakness was found practically | Re-read source and verify input formats |
| Missing SageMath | Some lattice attacks were unavailable | Use Sage only when evidence supports those attacks |
| FactorDB miss | No recorded factors were returned | Try evidence-driven local attacks |
| Fermat stalls | Factors are probably not close enough | Stop and choose a matching structural attack |
| Key recovered, output unreadable | Format, padding, byte order, or pairing is wrong | Inspect raw bytes and encryption source |
| Several candidates | Several interpretations succeeded | Validate padding, flag format, and re-encryption |
| General factoring stalls | Modulus may exceed bundled methods | Consider YAFU, msieve, or CADO-NFS only when justified |

Failure narrows the likely flaw; it is not a proof of security.

## 12. Validate Every Solution

Validate factors and derive `d` independently:

```python
from math import gcd

n = 0
e = 65537
p = 0
q = 0

assert p * q == n
phi = (p - 1) * (q - 1)
assert gcd(e, phi) == 1
d = pow(e, -1, phi)
print(d)
```

Validate plaintext by re-encryption:

```python
n = 0
e = 65537
c = 0
m = 0

assert pow(m, e, n) == c
```

Replace zeroes with challenge evidence. These checks catch copied digits, wrong factors, and mismatched ciphertexts.

## 13. Repeatable CTF Runbook

1. Record every `n`, `e`, `c`, key, ciphertext, and generation script.
2. Normalize public keys and confirm parameters with `--dumpkey`.
3. Infer the likely weakness from relationships, source, and hints.
4. Run the narrowest justified attack first.
5. Use automatic `--private` mode when several attacks are plausible.
6. Save factors, attack name, and recovered private key.
7. Decrypt while preserving raw bytes.
8. Identify and remove padding correctly.
9. Validate `p × q = n` and re-encrypt the plaintext.
10. Document why the construction failed, not only the command used.

## 14. Practice Scenarios

### One PEM Key, No Source

- Dump parameters.
- Note key size and `e`.
- Try automatic recovery.
- If FactorDB succeeds, document that it was a known factorization.

### Two Public Keys

- Compare exponents and moduli.
- Test for shared factors.
- If both encrypt the same message with small `e`, investigate broadcast conditions.

### `e = 3`, One Small Ciphertext

- Test for an exact integer cube root.
- If absent, seek additional recipients or a related-message construction.
- Do not blindly factor `n` when message size or missing padding is the weakness.

### Consecutive Prime Generator

- Predict close `p` and `q`.
- Prefer Fermat over general factoring.
- Confirm recovered factors multiply to `n`.

## Remediation Perspective

> 🛡️ **Remediation Note:** Generate RSA keys with a maintained cryptographic library and secure randomness. Use appropriately sized random primes, a standard exponent, OAEP for encryption, and PSS for signatures. Never reuse primes, invent prime-generation rules, expose partial private parameters, or use textbook RSA directly.

## Related

- [[Steganography And Cryptography Fundamentals]]
- [[Crypto101]]
- [Cryptography Blueprint](../blueprints/Cryptography%20Blueprint.md)
- [REV Python Toolkit](../tools/REV%20Python%20Toolkit.md)

## References

- [RsaCtfTool upstream README](https://github.com/RsaCtfTool/RsaCtfTool/blob/master/README.md)
- [RsaCtfTool repository](https://github.com/RsaCtfTool/RsaCtfTool)
- [RFC 8017: PKCS #1 v2.2](https://www.rfc-editor.org/rfc/rfc8017)

> Upstream command surface checked 2026-08-12. Always run `RsaCtfTool --help` because attack identifiers and arguments can change between releases.
