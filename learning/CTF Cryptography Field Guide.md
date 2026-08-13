# CTF Cryptography Field Guide

Use this learning note to recognize likely cryptographic weaknesses and choose an attack family. When you are actively solving, continue with the [Cryptography Blueprint](../blueprints/Cryptography%20Blueprint.md). For weak RSA challenges, use the [RsaCtfTool Guide](RsaCtfTool%20Guide.md).

> This module preserves and integrates the 2025 H4G cryptography notes from `cryptography_notes/cryptography_h4gnotes2025.md`.

## **0\. General Workflow for a Crypto Challenge**

1. **Identify the encoding first.** Base64, Base32, Base85, Hex, URL-encoding — chained encodings are common (CyberChef's "Magic" wand is great for this).  
2. **Identify the crypto primitive.** Look at key size, output length, and any given source code (chal.py, gen.py).  
3. **Read the source code carefully.** Most CTF crypto is "broken by design" — the vulnerability is almost always visible if given.  
4. **Check for known-weak parameters** — small e, reused nonce, small prime gaps, short key, ECB mode, etc.  
5. **Search the exact structure** (e.g. "RSA given n, e, c, and leaked p bits") — many challenges are variants of known CTF writeups.  
6. **Tools to always have installed:** pwntools, pycryptodome, sympy, sage (SageMath), openssl, CyberChef (offline or online), RsaCtfTool, John the Ripper, hashcat.

## **1\. Encoding vs Encryption (Basics)**

Encoding ≠ encryption — no key needed, fully reversible, meant for representation not secrecy.

| Encoding | Look for |
| :---- | :---- |
| Base64 | A-Za-z0-9+/=, length multiple of 4 |
| Base32 | A-Z2-7=, all uppercase |
| Base85/Ascii85 | Denser charset, often wrapped in \<\~ \~\> |
| Hex | 0-9a-f only |
| URL encoding | %XX sequences |
| ROT13/ROT47 | Looks like garbled English |
| Morse | Dots/dashes or .- patterns |
| Binary/Octal | Strings of 0/1 or 0-7 |

**Tip:** When a string "looks random but structured," try decoding blind with CyberChef Magic or base64 \-d, xxd \-r \-p, etc.

## **2\. Classical Ciphers (Basics)**

* **Caesar / ROT-N:** brute-force all 25/25 shifts.  
* **Vigenère:** repeating-key XOR-like cipher over letters. Attack via **Kasiski examination** (repeated substrings → key length) or **Index of Coincidence**, then frequency analysis per column.  
* **Substitution cipher:** frequency analysis (E, T, A, O, I, N most common in English); use quipqiup for automated solving.  
* **Rail Fence / Columnar Transposition:** rearrange, don't substitute — try all row counts.  
* **XOR cipher (single-byte key):** brute-force all 256 keys, score by printable-ASCII / English frequency.  
* **XOR cipher (repeating multi-byte key, "Vigenère XOR"):** find key length via Hamming distance between blocks (like breaking Vigenère), then solve each column as single-byte XOR. This is exactly how classic **repeating-key XOR** challenges (e.g., Matasano/Cryptopals Set 1\) are solved.

## **3\. Symmetric Cryptography (Intermediate)**

### **3.1 Stream ciphers / XOR**

* **Never reuse a one-time pad (OTP) key.** If two ciphertexts share a key: C1 XOR C2 \= P1 XOR P2 — crib-drag with likely words to recover plaintext.  
* **RC4 biases** exist (rarely shows up now, but classic WEP-style challenges use it).

### **3.2 Block ciphers (AES, DES, etc.)**

Know the **modes of operation** — the mode is usually the vulnerability, not the cipher itself:

| Mode | Weakness to exploit |
| :---- | :---- |
| **ECB** | Identical plaintext blocks → identical ciphertext blocks. Detected by repeated ciphertext blocks. Enables **ECB byte-at-a-time decryption** (build a dictionary of one-byte-short blocks) and **block shuffling/cut-and-paste** attacks. |
| **CBC** | Malleable — flipping a ciphertext byte flips the corresponding byte in the *next* plaintext block predictably (**bit-flipping attacks**). No built-in integrity check. |
| **CBC \+ Padding Oracle** | If the server leaks "padding valid/invalid" (via error message or **timing**), you can decrypt (and even encrypt/forge) *any* ciphertext byte-by-byte without the key — the classic **Padding Oracle Attack** (Vaudenay). Tool: padbuster, or PadBoi. Also test for a *timing* oracle when there's no explicit error message. |
| **CTR** | Turns block cipher into a stream cipher — **nonce reuse** is catastrophic (same keystream XORed against two plaintexts → XOR them together like OTP reuse). |
| **GCM** | Provides authentication (AEAD). **Nonce reuse in GCM is catastrophic** — leaks the authentication key and allows forgery. |

### **3.3 Key/IV mistakes to always check for**

* Hardcoded or predictable IV (e.g., all-zero IV, IV \= key).  
* Key derived from a short/guessable password (brute-force offline with hashcat).  
* Key reuse across multiple messages/nonces.

### **3.4 Hashing**

* **Length extension attacks**: if a MAC is computed as H(secret || message) using MD5/SHA1/SHA256 (Merkle–Damgård construction), an attacker can append data and compute a valid new hash *without knowing the secret*. Tool: hashpump. **HMAC is NOT vulnerable** to this — always look for whether it's H(key||msg) vs proper HMAC.  
* **Hash collisions**: MD5 and SHA1 are broken for collision resistance (not preimage) — tools like HashClash produce colliding files.  
* **Cracking hashes**: identify hash type (hashid, hash-identifier), then hashcat/John with wordlists \+ rules if it's a weak/salted password hash.

## **4\. RSA — the CTF Favorite (Intermediate → Advanced)**

Core: n \= p\*q, public (n, e), private d, c \= m^e mod n, m \= c^d mod n, φ(n) \= (p-1)(q-1), d \= e^-1 mod φ(n).

**Always start by checking:**

* Is n small enough to factor? → **Fermat / Pollard's p-1 / Pollard's rho / trial division** (try RsaCtfTool first; factordb.com has been unreliable/unavailable lately — see the note in §13 for fallback options).  
* Is e small (e.g., e=3) with no padding and a short message? → **Cube root attack**: if m^3 \< n, just take the integer cube root of c.  
* Are multiple ciphertexts encrypted with the **same message, different moduli, same small e**? → **Håstad's Broadcast Attack** (CRT to combine, then take root).  
* Is the **same n, different e** used to encrypt the **same message** to two people? → **Common Modulus Attack** (use extended Euclidean algorithm on the two e values).  
* Are p and q close together? → **Fermat factorization** (n \= a² − b²).  
* Is d small relative to n? → **Wiener's Attack** (continued fractions) — works when d \< N^0.25 roughly.  
* Are some bits of p, q, or d leaked/partial? → **Coppersmith's method** (lattice-based, via Sage).  
* Is the same n reused across multiple key pairs, and do you have two ciphertexts with **shared prime factors** across different n values? → **GCD attack**: gcd(n1, n2) reveals a shared prime.  
* Is it **RSA with a small private exponent / partial key exposure**? → Coppersmith's short-pad / related-message attacks.  
* Chinese Remainder Theorem (CRT) with faulty signature (bad padding in one of the CRT computations) → **Bellcore/fault attack** on RSA-CRT signatures.

**Quick tool:** RsaCtfTool automates most of the above — always run it first if you have n, e, c. It has a \--attack factordb option, but since factordb.com itself has been down/unreliable, skip that flag and let it fall through to its local attacks (Fermat, Pollard, Wiener, etc.), or run sympy.factorint(n) / SageMath's factor(n) directly for small-to-medium n.

## **5\. Diffie–Hellman & Discrete Log (Intermediate → Advanced)**

* Classic DH: g^a mod p exchanged, shared secret g^(ab) mod p.  
* **Small subgroup / weak p**: if p-1 has only small prime factors ("smooth"), use **Pohlig–Hellman** to solve the discrete log efficiently.  
* **Small p in general**: brute-force discrete log directly, or use **Baby-step Giant-step / Pollard's rho for discrete log**.  
* **Static/reused private key across sessions** can leak via side channels or protocol misuse.

## **6\. Elliptic Curve Cryptography (Advanced)**

* ECDSA: signature \= (r, s). **Nonce (k) reuse across two signatures** leaks the private key (solve two linear equations). This is the classic **PS3/Sony ECDSA bug**.  
* **Biased or partially-known nonces** (e.g., LSBs leaked) → lattice attack (**Hidden Number Problem**, via Sage's LLL).  
* **Invalid curve attacks**: sending a point not actually on the curve to a naive implementation can leak the private key.  
* **Small-order / singular curves**: some CTF challenges use deliberately weak curve parameters — check curve order factorization for small factors → Pohlig–Hellman.  
* Tools: sage, fault\_attack scripts, ecdsa python lib for verification.

## **7\. Lattice Attacks (Advanced)**

Lattice reduction (**LLL**, **BKZ** algorithms, via SageMath's Matrix(...).LLL()) is the go-to for:

* Coppersmith's attack (partial key/message exposure in RSA).  
* Wiener's attack (can be reframed as a lattice/continued-fraction problem).  
* ECDSA nonce-bias attacks (Hidden Number Problem).  
* **Knapsack cryptosystems** (Merkle–Hellman) — solvable via lattice basis reduction.  
* NTRU / lattice-based post-quantum challenges (LWE, Ring-LWE) — usually intentionally "toy-sized" in CTFs so LLL/BKZ can brute the short vector.

## **8\. Quantum Cryptography (as seen in CTFs — QKD/BB84)**

* **BB84 protocol basics:** sender (Alice) encodes bits in random bases (rectilinear \+ or diagonal ×); receiver (Bob) measures in random bases; they publicly compare *bases* (not values) and keep only matching-basis bits (**sifted key**).  
* **Common CTF angles:**  
  * Eavesdropper (Eve) intercept-resend introduces detectable errors (\~25% QBER) — challenges often ask you to compute/detect this.  
  * Simulate the protocol given a transcript of bases/measurements and reconstruct the shared key.  
  * Exploit **implementation flaws** (not the protocol itself) — e.g., predictable "randomness," or a flawed simulator that leaks basis info early.  
* These challenges are usually **simulation/logic puzzles** around the protocol rather than attacks on real quantum hardware — read the challenge's Python/Qiskit source carefully for where randomness or classical-channel data leaks state it shouldn't.

## **9\. PRNG / Randomness Attacks (Intermediate → Advanced)**

* **Predictable seeds**: random.seed(time.time()) or a small seed space → brute-force.  
* **Python's random (Mersenne Twister) is NOT cryptographically secure** — given 624 consecutive 32-bit outputs, you can clone the entire internal state (tools: randcrack) and predict all future/past outputs.  
* **LCGs (Linear Congruential Generators)**: recoverable from a handful of outputs via basic algebra if the modulus/multiplier are known or guessable.  
* Always check: is the "random" key/nonce actually derived from something guessable (timestamp, PID, weak seed)?

## **10\. Password / Key File Cracking (Practical — relevant to your KeePass work)**

* **Identify the format** first: .kdbx (KeePass), zip, pdf, office docs, luks, ssh keys, etc.  
* Extract a crackable hash using the matching \*2john tool (e.g., keepass2john, zip2john, office2john, ssh2john, rar2john).  
* Crack offline with **hashcat** (GPU, faster, use \--example-hashes to find the right mode number) or **John the Ripper** (CPU, easier for custom rules).  
* Use targeted wordlists (rockyou.txt, custom lists built from challenge context) \+ rule-based mutations (best64.rule, OneRuleToRuleThemAll.rule) rather than blind brute force when possible.  
* If it's a **key-file \+ password** combo (like KeePass2), both matter — check if the key file is embedded/derivable from challenge files.

## **11\. Digital Signatures & PKI (Advanced)**

* **Signature malleability / verification bugs**: some naive verifiers use \== on raw bytes without proper padding checks (Bleichenbacher's e=3 RSA signature forgery — PKCS\#1 v1.5 with weak verifiers).  
* **JWT attacks** (common in web+crypto crossover challenges):  
  * alg: none — some libraries accept unsigned tokens.  
  * **RS256 → HS256 confusion**: if the server verifies with the public key as an HMAC secret, you can forge tokens once you have the public key.  
  * Weak/guessable HMAC secret → crack with hashcat/jwt\_tool.  
* **Certificate chain issues**: self-signed root trust, expired cert acceptance, hostname bypass.

## **12\. Steganography-adjacent Crypto**

Sometimes "crypto" challenges hide the ciphertext itself:

* Check file metadata (exiftool), LSB steganography (zsteg, stegsolve), and appended data after EOF markers (binwalk, foremost).  
* Once extracted, re-apply the crypto analysis above.

## **13\. Quick-Reference Toolbox**

| Purpose | Tool |
| ----- | ----- |
| Encoding identification | CyberChef |
| RSA automated attacks | RsaCtfTool (run with \--attack all) |
| Factoring (factordb alternative) | sympy.factorint(), sage's factor(), Pollard rho/p-1 scripts, yafu, msieve (GNFS for larger semiprimes) |
| Big number math / factoring | sympy, sage |
| Lattice reduction | SageMath (LLL, BKZ) |
| Padding oracle | padbuster, custom pwntools script |
| Hash identification | hashid, name-that-hash |
| Password/hash cracking | hashcat, John the Ripper |
| File-to-hash extraction | \*2john suite |
| PRNG state recovery (Python) | randcrack |
| Length extension | hashpump |
| JWT attacks | jwt\_tool |
| General scripting | Python \+ pycryptodome \+ pwntools |
| ECDSA/curve math | SageMath, ecdsa (Python) |
