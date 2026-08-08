# ROT1 Cipher

> Source: [https://www.dcode.fr/rot1-cipher](https://www.dcode.fr/rot1-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is ROT1? (Definition)

The ROT1 cipher is a substitution cipher based on a shift of one (1) letter in the alphabet. Each letter is therefore replaced by the next ( A becomes B , B becomes C , etc.).

This shift is the basis of the Caesar code and its variants, sometimes the shift of 1 is called the Augustan code.

## How to encrypt using Rot cipher?

All letters in the plaintext are replaced by those immediately following in the alphabet ( A becomes B , B becomes C , etc. and for the last letter Z , the alphabet is considered a loop and the letter following Z is therefore A , the first letter)

Initial alphabet ABCDEFGHIJKLMNOPQRSTUVWXYZ Alphabet shifted by ROT1 BCDEFGHIJKLMNOPQRSTUVWXYZA

Initial alphabet ABCDEFGHIJKLMNOPQRSTUVWXYZ Alphabet shifted by ROT1 BCDEFGHIJKLMNOPQRSTUVWXYZA

Example: The message ROTATION is coded SPUBUJPO

ROT1 code only supports letters of the standard Latin alphabet (A-Z, a-z). Special characters and punctuation are ignored. Optionally, digits can also be shifted by 1.

## How to decrypt Rot1 cipher?

Rot1 decryption is similar to encryption but uses the opposite shift by replacing each letter with the one immediately before in the alphabet (and the letter before A is the letter Z as if the alphabet was a loop).

Alphabet shifted by ROT1 ABCDEFGHIJKLMNOPQRSTUVWXYZ Plain alphabet ZABCDEFGHIJKLMNOPQRSTUVWXY

Alphabet shifted by ROT1 ABCDEFGHIJKLMNOPQRSTUVWXYZ Plain alphabet ZABCDEFGHIJKLMNOPQRSTUVWXY

Example: The message BMQIBCFU is decoded ALPHABET

## How to program Rot1 functions?

The algorithm for encryption and decryption of ROT1 is: // Pseudo-code Function encrypt(text) { alphabet = {A:B, B:C, .., Y:Z, Z:A} ciphertext = '' for each character c in text { ciphertext += alphabet[c] } return ciphertext } Function decrypt(text) { alphabet = {A:Z, B:A, C:B, .., Z:Y} plaintext = '' for each character c in text { plaintext += alphabet[c] } return plaintext } // Python def rot1(text): return ''.join(chr(ord(c) + 1) if 'A' <= c <= 'Y' else ('A' if c == 'Z' else 'a') for c in text)
