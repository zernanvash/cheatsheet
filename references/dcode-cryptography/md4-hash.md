# MD4

> Source: [https://www.dcode.fr/md4-hash](https://www.dcode.fr/md4-hash)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is MD4? (Definition)

The MD4 for ( Message Digest 4 ) is an old hash function . MD4 associates an input data with a binary hash according to a one-way hash (it is practically impossible to perform the reverse operation).

## How to encrypt in MD4?

The MD4 hash computes a 128 bit digital fingerprint (32 hexadecimal characters) from binary computer data.

Example: dCode code is 31f5516dab1958c00d5eda6637333575

The MD4 algorithm is described in RFC 1186 then RFC 1320.

## How to decrypt MD4 cipher?

The MD4 uses non-linear functions whose purpose is to be non-reversible, so there is no decoding method.

However, it is conceivable (with sufficient time and computing power) to test all the possible words and compare their fingerprint with that sought.

Databases containing pre-computed MD4 hashes are called rainbow tables.

dCode uses a rainbow table (2 million passwords), if the desired MD4 is not present, then the decryption will fail.

## How to recognize MD4 ciphertext?

The MD4 hash is visually identical to the MD5 (128 bits) generally written in the form of 32 hexadecimal characters 0123456789abcdef .

The MD4 was used to store NTLM password fingerprints on Windows.

The empty string has for hash 31d6cfe0d16ae931b73c59d7e0c089c0

## What is a MD4 collision?

The MD4 has been tested by researchers who found collisions (2 different chains that have the same footprint).

Example: hexadecimal values 839c7a4d7a92cb5678a5d5b9eea5a7573c8a74deb366c3dc20a083b69f5d2a3bb3719dc69891e9f95e809fd7e8b23ba6318edd45e51fe39708bf9427e9c3e8b9 and 839c7a4d7a92cbd678a5d529eea5a7573c8a74deb366c3dc20a083b69f5d2a3bb3719dc69891e9f95e809fd7e8b23ba6318edc45e51fe39708bf9427e9c3e8b9 have the same MD4 hash: 4d7e6a1defa93d2dde05b45d864c429b

Its use is not recommended today for password storage, even when using salt.

## What does the MD4 acronym mean?

MD4 stands for Message Digest 4 , which can be understood as message summary version 4.

## When was MD4 invented?

MD4 was proposed by Ronald Rivest in October 1990
