# Vernam Cipher (One Time Pad)

> Source: [https://www.dcode.fr/vernam-cipher](https://www.dcode.fr/vernam-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is the Vernam cipher? (Definition)

The Vernam cipher is a symmetric encryption method that combines a plaintext message with a secret key. In its most rigorous form, called a one-time pad, it guarantees perfect security in the information theory sense: the ciphertext reveals no information about the plaintext.

This security is ensured only if three conditions are met:

— the key is perfectly random

— the key has the same length as the message

— the key is used only once

The system was formalized by Gilbert S. Vernam in 1917 for encrypting telegraphic communications (Baudot cipher) using an XOR operation (bit-by-bit modulo-2 addition ). However, the method is applicable to various key ciphers, such as the Vigenère cipher .

## How to encrypt using Vernam (Vigenere) cipher?

The Vernam cipher can use the Vigenère cipher method, but with a completely random encryption key that must have the same number of letters (or even more) than the number of characters in the plaintext message.

Example: To encrypt DCODE , a key of at least 5 letters is needed ( KEYWORD , PASSWORD , etc).

If the key is not long enough, it will be repeated, as in the Vigenere cipher , but this introduces a cryptographic weakness in the message.

## How to encrypt using Vernam (XOR) cipher?

The Vernam cipher can use the XOR encryption method, but with a randomn encryption key that must have a bit size identical to (or greater than) the bit size of the plain message.

Example: To encrypt 010101 , a key of at least 6 bits is required.

## How to decrypt a Vernam ciphertext?

Decryption depends on the encryption method used, Vernam makes no changes to the usual decryption.

## How to decipher Vernam (Vigenere) without key?

In the case of a true one-time pad (a random key, as long as the message and used only once), keyless decryption is impossible, even with infinite computing power.

This result was demonstrated by Claude Shannon : the system possesses perfect security.

However, if the three conditions are not met, the system becomes vulnerable to various forms of cryptanalysis.

## Why is the one time pad considered unbreakable?

The one-time pad is perfectly secure because, for a given ciphertext, every possible plaintext has exactly the same probability of being correct if the key is random.

In other words, the ciphertext can correspond to an infinite number of different, equally plausible messages.

This means that an attacker cannot obtain any information about the plaintext without knowing the key.

## When Vernam cipher was invented?

First example were found at the end of the 19th century and Vernam described it in 1917.
