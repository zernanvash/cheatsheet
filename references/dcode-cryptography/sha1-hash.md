# SHA-1

> Source: [https://www.dcode.fr/sha1-hash](https://www.dcode.fr/sha1-hash)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is SHA-1? (Definition)

SHA-1 (for Secure Hash Algorithm 1) is a cryptographic hashing algorithm developed by the NSA that transforms a variable-size data entry into a fixed 160-bit fingerprint (40 hexadecimal characters). This fingerprint is designed to be unique and deterministic: the same entry will always produce the same hash, this ensures the integrity of the initial data (a file or a message).

## How to decrypt a SHA-1 hash?

As encryption is a hashing based on nonlinear functions, there is no decryption method . This means that to retrieve the password corresponding to a sha-1 hash , there is no choice but to try all possible passwords!

Technically, this operation would take several thousand years, even on the most powerful computers in the world. However, the list of passwords used in real life is more restricted, and it becomes possible to precalculate the most likely fingerprints.

dCode uses its word databases (10 million potential passwords) to speed up this processing. However, if the password is rare, or combined with salting, it will probably not be found.

## How to recognize SHA-1 fingerprint?

The hash is composed of exactly 40 hexadecimal characters among 0123456789abcdef .

More rarely the hash is stored as a 20-byte binary string.

## What are the variants of the SHA-1 cipher?

The database search can be complicated by inserting a salt to the word. The salt is usually a prefix or a suffix. Indeed, if it is already difficult but possible to precalculate the fingerprints of all the words, it becomes even more difficult to precalculate with all possible prefixes and suffixes.

Example: SHA1 ( dCode ) = 15fc6eed5ed024bfb86c4130f998dde437f528ee but SHA1 ( dCodeSUFFIX ) = 9b63fcb31388acee8879018244a3d107033890f1

Another (not recommended) variant is DOUBLE SHA1 , that consists in applying SHA1 twice (the first time on the original string, then the second time on the computed hash).

## What is a rainbow table?

A rainbow table is a database of words with all the pre-computed hashes and stored in order to accelerate and be able to parallelize the calculations of fingerprints.

## What is the list of SHA1 Magic Hashes for PHP?

List of magic SHA-1 hashes :

String MD5 (String) aa3OFF9m 0e36977786278517984959260394024281014729 aaK1STfY 0e76658526655756207688271159624026011393 aaO8zKZF 0e89257456677279068558073954252716165668 aaroZmOk 0e66507019969427134894567494305185566735

String MD5 (String) aa3OFF9m 0e36977786278517984959260394024281014729 aaK1STfY 0e76658526655756207688271159624026011393 aaO8zKZF 0e89257456677279068558073954252716165668 aaroZmOk 0e66507019969427134894567494305185566735

Bonus magic SHA-1 like string that can also be evaluated at 0 : 0e00000000000000000000081614617300000000 or 0e00000000000000000000721902017120000000

## Why is SHA-1 considered less secure?

The SHA-1 algorithm was widely used before security flaws limited its use in contexts requiring high security.

In 2017, a team of researchers from Google and CWI Amsterdam publicly demonstrated a practical SHA-1 collision, named SHAttered here

These flaws allow an attacker to create two different messages with the same hash, bypassing the integrity guarantees offered by the hash function .

More robust algorithms such as SHA-256 or SHA-3 are now recommended.

## What does SHA1 letters mean?

SHA1 stands for Secure Hash Algorithm (version 1)

## When was SHA1 invented?

SHA1 was proposed by the National Security Agency in 1995.
