# SHA-256

> Source: [https://www.dcode.fr/sha256-hash](https://www.dcode.fr/sha256-hash)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is the SHA-256? (Definition)

SHA-256 (Secure Hash Algorithm - 256 bits) is a cryptographic hash function belonging to the SHA-2 family, standardized by the NIST (National Institute of Standards and Technology) in the United States.

It allows any binary data (text, file, message) to be associated with a fixed-size digital fingerprint: 256 bits, generally represented by 64 hexadecimal characters.

This fingerprint characterizes the data deterministically and with an extremely low probability of collision.

Example: dCode has for hash 254cd63ece8595b5c503783d596803f1552e0733d02fe4080b217eadb17711dd

## How to encrypt a character string using SHA256?

The SHA-256 algorithm works in several steps:

— convert the string to binary

— add padding

— divide the message into 512-bit blocks

— apply a compression function to each block

These mechanisms ensure a strong avalanche effect: a minimal change to the input results in a near-total change to the hash.

Example: SHA-256 is coded as' bbd07c4fc02c99b97124febf42c7b63b5011c0df28d409fbb486b5a9d2e615ea and SHA256 '(without hyphen) is coded as' b3abe5d8c69b38733ad57ea75e83bcae42bbbbac75e3a5445862ed2f8a2cd677' (57 changed characters out of 64)

## How to decrypt SHA256 cipher?

SHA-256 , like all cryptographic hash functions , is irreversible: there is no decryption method that allows for the direct recovery of the original message.

The only possible approaches involve testing candidates (dictionary or brute-force attacks) and comparing their hash to the target hash.

dCode uses databases of words or passwords whose hashes are already known.

If the requested hash matches a pre-calculated value, the original string can be recovered; otherwise, decryption will fail.

In the presence of salting (modification of the input string by adding a value), this type of attack becomes much more difficult, if not impossible.

## How to generate a SHA256 hash starting or ending with 0000?

The bits/characters composing a hash are not predictable. It is also a property used in the concept of proof of work (PoW) used by the blockchain. The only method to date being to test combinations by brute force, until finding a particular case that works.

## How to recognize SHA256 ciphertext?

The hash is composed of 64 hexadecimal characters 0123456789abcdef (ie 256 bits)

The context of use (blockchain, Bitcoin, digital signatures, file integrity) is often a determining factor in identifying SHA-256 .

## How does the SHA-256 compression function work?

The compression function relies on non-linear logical operations on 32-bit words, such as:

$$ \operatorname{Ch}(E,F,G) = (E \wedge F) \oplus (\neg E \wedge G) $$

$$ \operatorname{Ma}(A,B,C) = (A \wedge B) \oplus (A \wedge C) \oplus (B \wedge C) $$

$$ \Sigma_0(A) = (A\!\ggg\!2) \oplus (A\!\ggg\!13) \oplus (A\!\ggg\!22) $$

$$ \Sigma_1(E) = (E\!\ggg\!6) \oplus (E\!\ggg\!11) \oplus (E\!\ggg\!25) $$

## What constants are used in SHA-256?

The SHA-256 algorithm uses 64 constants derived from the fractional parts of the cube roots of prime numbers. Here is the list:

0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5, 0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174, 0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da, 0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967, 0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85, 0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070, 0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3, 0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2

## What is the maximum length of a character string for SHA-256?

SHA-256 has no practical limit on character string length .

Potentially, beyond 2.3 exabytes (2^64 bits), there should be a cryptographic limit.

The actual limit depends on the available memory on the system performing the calculation.

## What is the probability of collision with SHA-256?

A collision occurs when two different messages produce exactly the same hash fingerprint with a given hash function .

A SHA-256 hash has 2^256 possible values. Assuming that SHA-256 behaves like an ideal random function, according to the birthday paradox , it would take approximately 4.0 × 10^38 distinct messages to have a collision probability of 50% (which far exceeds any current computing capacity).
