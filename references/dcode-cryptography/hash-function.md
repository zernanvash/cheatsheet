# Hash Function

> Source: [https://www.dcode.fr/hash-function](https://www.dcode.fr/hash-function)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is a hash function? (Definition)

A hash function is an algorithm that takes data of any size as input and transforms it into a fixed-size value, called a fingerprint or hash . This transformation is unidirectional, which means that it is difficult (if not impossible) to return to the original data from the hash (which is very useful in computer science and cryptography).

## What is a hash? (Definition)

The hash is the fingerprint result of the hash function .

Example: dCode has for hash MD5 e9837d47b610ee29399831f917791a44

Example: dCode has for hash SHA1 15fc6eed5ed024bfb86c4130f998dde437f528ee

Example: dCode has for fingerprint SHA256 254cd63ece8595b5c503783d596803f1552e0733d02fe4080b217eadb17711dd

## Why using a a hash?

The hash is the fingerprint result of the hash function , it identifies with a high probability the initial data without having to store it. This allows you to verify a password, without needing to know it.

Small changes in the input data lead to drastic changes in the resulting hash. This ensures data integrity and helps to check whether the data has been tampered with.

## How to calculate/encode a hash?

The hash functions use computer data ( in binary format) and apply nonlinear and non-reversible functions with a strong avalanche effect (the result is very different even if the input data is very similar). The fingerprint is usually returned as hexadecimal characters.

See the dCode pages for each hash function to know how it works in detail: MD5 , SHA1 , SHA256 , etc.

## How to decrypt a hash?

The principle of hashing is not to be reversible, there is no decryption algorithm, that's why it is used for storing passwords: it is stored encrypted and not unhashable.

Example: 123+456=579 , from 579 how to find 123 and 456 ? This is not possible except by trying all possible combinations .

The hash functions apply millions of non-reversible operations so that the input data can not be retrieved.

Hash functions are created to not be decrypted, their algorithms are public. The only way to decrypt a hash is to know the input data.

## What are rainbow tables?

Theoretically, a brute-force mode is possible by testing all the binary strings, but a short message of 6 bytes already represents 281,000 billion combinations . Even with fast processors capable of performing millions of hash calculations per second, several days, months or years of calculations are therefore necessary to try all the possibilities in order to find a single hash.

However, users generally always use the same passwords and some characters more than others, so it is possible to store the most likely binary strings and their respective hashes in a very large dictionary. These dictionaries are called rainbow tables. These tables make it possible to test all the words of a given dictionary to check if their fingerprint corresponds to a given one.

Example: dCode uses its word and password databases with millions of pre-calculated hashes.

If the word is not in the base/dictionary, then there will be no result.

## How to recognize a hash?

A hash can take many forms, but the most common are hexadecimal strings: 32 characters 0123456789abcdef for the MD5 , 40 for the SHA-1 , 64 for the SHA-256 , etc.

The encoding system based on crypt () functions uses the symbol $ followed by a number indicating the algorithm used and its possible parameters.

dCode has a hash identifier .

## What is salt (for a hash)?

The rainbow tables (gigantic databases of hash and password matches) are growing day by day and accumulating passwords stolen from various sites, and taking advantage of the computational performance of super calculators, allow today to decipher short passwords in minutes / hours.

In order to counter this technique, it is recommended to add salt (some characters in prefix or suffix) to the password/message. In this way, the precalculated tables must again be calculated to account for the salt that systematically modifies all the fingerprints, the salting step. Passwords are salted .

Example: MD5 ( dCode ) = e9837d47b610ee29399831f917791a44 and MD5 ( dCodeSUFFIX ) = 523e9a80afc1d2766c3e3d8f132d4991

## What is a cost (for a hash)?

Cost is the measure of the resources needed to calculate a hash. In order to complicate the task of creating the rainbow tables, it is possible to complicate some hashes so that the calculations take several milliseconds or seconds, which makes the duration necessary for the attacks too great to be applicable.

## What is bcrypt?

bcrypt is a library of cryptographic functions that applies recursion rules to hash functions . Natively, the notions of salt and cost are applicable.

## What is the difference between a secure hash and a fast hash?

A secure hash is calculated with a high cost, which makes the process slower and more resource intensive. This makes it more resistant to brute force attacks.

In contrast, a fast hash is calculated faster but is potentially more vulnerable to attacks.
