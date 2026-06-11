# Steganography And Cryptography Fundamentals

Use this before the stego and crypto blueprints. The goal is to classify what kind of puzzle you are holding before choosing tools.

## Steganography Basics

Steganography hides data inside another file or medium.

Common carriers:

- images
- audio
- video
- PDFs
- archives
- whitespace/text
- metadata

First checks:

```bash
file sample
exiftool sample
strings -n 8 sample
binwalk sample
```

Ask:

- Is the extension honest?
- Is there metadata?
- Are there embedded files?
- Is there appended data?
- Does the image/audio have visible or audible oddities?
- Is there a password hint?

## Cryptography Basics

Cryptography challenges usually involve encoding, encryption, hashing, or broken custom code.

Classify first:

- Encoding: Base64, hex, URL, binary, Morse. Reversible without a key.
- Encryption: needs a key or broken design.
- Hashing: one-way; crack only if weak/common or with a wordlist.
- Custom code: reverse the algorithm instead of guessing.

First checks:

```bash
file data
strings -n 8 data
xxd data | head
```

## Python Mindset

Use Python when the task repeats:

- XOR each byte.
- Decode many layers.
- Try Caesar shifts.
- Reverse index shuffles.
- Test a small keyspace.
- Parse integers for RSA.

## Web Tools

Use web tools only for CTF/lab data:

- CyberChef for encoding chains and quick transforms.
- dCode for classical ciphers.
- FactorDB for small RSA modulus checks.
- StegOnline/Aperi'Solve for visual image stego.

## When To Jump To Blueprints

- Hidden data in files -> [Steganography Blueprint](../blueprints/Steganography%20Blueprint.md).
- Cipher/hash/custom math -> [Cryptography Blueprint](../blueprints/Cryptography%20Blueprint.md).
- Archive cracking -> [Archive And Password Manager Cracking](../blueprints/machine-attacks/Archive%20And%20Password%20Manager%20Cracking.md).
- Byte transform -> [REV Python Toolkit](../tools/REV%20Python%20Toolkit.md).
