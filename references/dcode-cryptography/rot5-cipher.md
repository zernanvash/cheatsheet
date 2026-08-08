# ROT-5 Cipher

> Source: [https://www.dcode.fr/rot5-cipher](https://www.dcode.fr/rot5-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is the ROT-5 Cipher? (Definition)

The ROT-5 cipher is a simple encryption method that involves shifting each digit 5 positions in 0123456789 .

NB: it can also involve shifting letters 5 positions in the alphabet (see ROT cipher ).

## How to encrypt using Rot5?

ROT5 encryption applies on the digits in a message (ideally made of numbers). It consists in replacing a digit by another by adding 5 ( modulo 10 ).

1234567890 6789012345

Example: 248 is encrypted 793 by ROT-5

For letters, the similar cipher method is ROT13

## How to decrypt Rot-5 cipher?

Decryption of Rot5 is identical to the encryption because Rot5 is reversible.

6789012345 1234567890

Example: 793 re-becomes 248 by ROT-5

## How to recognize ROT-5 ciphertext?

ROT-5 converter is used on the digits. Numbers that began with 1 now begin with 6, the 2s become 7s etc. The shifting by 5 continues so on.

According to Benford's law , there should be more 6 than 4 among the first digits of the numbers in the ciphertext.

## What are the variants of the Rot-5 cipher?

Rot-5 is already a variant of Rot13 , itself a version of Caesar cipher with a shift of 13. Rot-5 is therefore a Caesar cipher with a shift of 5, but applied to an alphabet of digits.

It is common to associate a ROT-13 for coding the letters and ROT-5 for the numbers at the same time.

## What a shift of 5 for Rot5?

A shift of 5 allows the code to be reciprocal/reversible/symmetric, this means that 2 consecutive encryptions lead to find the plain number.
