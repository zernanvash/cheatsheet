---
source: ../references/Crypto101 Full Text Archive.md
author: Laurens Van Houtven (lvh)
license: "CC BY-NC 4.0 - https://creativecommons.org/licenses/by-nc/4.0/"
original_url: "https://www.crypto101.io/"
tags: [cryptography, course, XOR, AES, RSA, TLS, hash, MAC]
last_updated: 2026-08-08
---
# Crypto 101 Course

> **Primary source:** Laurens Van Houtven, *Crypto 101*, version 0.6.0-95-g64e8ccf, migrated into the offline course-book reader.  
> **License:** [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/).  
> **Course page:** [Open the searchable offline course](../crypto101-course.html).

This is the vault's learning-oriented entry point to *Crypto 101*. It combines short lessons with the complete migrated book text, including objectives, mental models, key terms, checkpoints, chapters, subsections, glossary, references, and retained figures. No PDF reader or network connection is required.

## Recommended Path

1. Start with XOR, block ciphers, and stream ciphers.
2. Continue through key exchange, public-key encryption, hashes, MACs, signatures, KDFs, and RNGs.
3. Study TLS, OpenPGP, and OTR to see how primitives become systems.
4. Use the math and side-channel appendices when a lesson needs them.
5. Pair the course with the [Cryptography Blueprint](../blueprints/Cryptography%20Blueprint.md) during CTF work.

## Course Modules

| Track | Lessons | Original print pages |
|---|---|---:|
| Foundations | XOR; block ciphers; stream ciphers and modes | 17–80 |
| Trust and identity | Key exchange; public-key encryption; hashes; MACs; signatures | 81–136 |
| Key material | KDFs; random number generators | 137–161 |
| Complete systems | SSL/TLS; OpenPGP/GPG; OTR | 163–184 |
| Math and implementation | Modular arithmetic; elliptic curves; side channels | 186–205 |

## Preserved Source Material

- [Complete course-book reader](../crypto101-course.html) — the primary searchable reading experience.
- [Preserved full-text archive](../references/Crypto101%20Full%20Text%20Archive.md) — retained as the local source of record and for rebuilding the structured reader.

> 💡 **What to watch out for:** The book explains historical algorithms and protocol attacks for learning. Treat age-sensitive configuration advice as historical context and verify current deployment guidance separately.
