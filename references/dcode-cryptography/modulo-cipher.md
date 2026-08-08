# Modulo Cipher

> Source: [https://www.dcode.fr/modulo-cipher](https://www.dcode.fr/modulo-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is a Modulo cipher? (Definition)

A modulo cipher uses modular calculus on numbers in order to extract the remainder. The values obtained can then be used as a code/index for another cipher such as A1Z26 or the ASCII code .

## How to encrypt using Modulo cipher?

Modulo Cipher Encryption uses modular arithmetics and a sequence of numbers, characters must be converted into numbers, e.g. A=1 , B=2 , … Z=26 , but any numeric conversion (like the ASCII table ) is fine.

Example: To crypt DCODE with the modulo 26 , convert the text to numbers 4,3,15,4,5 .

For each number to encrypt, calculate a random number which value is equal to the number to crypt .

Example: For $ 4 $, take $ 654 $, as $ 654 \equiv 4 \ mod 26 $ For $ 3 $, take $ 965 $, as $ 965 \equiv 3 \ mod 26 $. The encrypted message is 654,965,561,732,941 (many other cipher message are possible)

## How to decrypt Modulo cipher?

Decryption requires to know the value of the Modulo and to know the series of number to decrypt.

Example: The encrypted message is 654,965,561,732,941 with the modulo 26 .

For each number N , calculate the value of the remainder in the euclidean division of N by the modulo to get the plain number.

Example: The plain text is 4,3,15,4,5 , that can be translate into DCODE with A1Z26 (A=1, B=2, etc.)

## How to recognize Modulo ciphertext?

The ciphered message is constituted of somehow large random numbers .

## What are the variants of the Modulo cipher?

The Affine cipher use modulo in the calculation $ C = a \times P + b \mod 26 $
