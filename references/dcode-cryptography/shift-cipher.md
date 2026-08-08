# Shift Cipher

> Source: [https://www.dcode.fr/shift-cipher](https://www.dcode.fr/shift-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is a Shift cipher? (Definition)

Shift cipher is a monoalphabetic substitution technique where each letter of the original message is replaced by another letter, shifted by a fixed number of positions in the alphabet .

This number of positions, expressed as an integer, is called the (shift) key .

The Caesar cipher is the best-known example of a shift cipher, classically illustrated with a key of value 3.

## How to encrypt using the shift cipher?

Shift ciphers use an alphabet and a shift key that alters the position of letters within it.

For example, if a letter is located at position $ N $ in the alphabet , applying a shift of $ X $ replaces it with the letter located at position $ N+X $. This is equivalent to using a shifted alphabet as a substitution table.

Example: Take the letter E in position 5 in the alphabet ABCDEFGHIJKLMNOPQRSTUVWXYZ , it will be encrypted by a shift of 3 in position 8 or H .

When the new position exceeds the length of the alphabet, restart the alphabet from the beginning, as the alphabet is considered cyclic.

Example: Z shifted by 1 gives A .

Traditional shift ciphers only apply to the 26 letters of the Latin alphabet. Numbers, spaces, or special characters can be excluded from the encryption, left unchanged, or included via an extended alphabet.

## What are the different possible shifts?

It is possible to define different types of shifts, some shifts correspond to known encryption algorithms:

A single shift (all letters are shifted by the same value) is called Caesar Code .

A multiple shift , according to a sequence or a key that is repeated (the letters are shifted from each of the key values), is called Vigenere Cipher .

A mathematical shift , the easier is progressive, shifting the nth letter of the value n is the Trithemius Cipher or if the shift is more complex Affine Cipher or even Hill Cipher.

In addition , each offset can be applied to a single or several letters, to a single or several words, etc.

## How to decrypt using the shift cipher?

Decryption requires knowing the shift used and the alphabet.

Take a letter in position N in the alphabet that has been encrypted by a shift of X , it must be shifted by -X to return to its original position N-X .

Example: The letter H in position 8 in the alphabet ABCDEFGHIJKLMNOPQRSTUVWXYZ , will be decrypted from a shift of 3 in position 8-3=5 or E .

Example: The word TIJGU is decoded with an offset of 1 as SHIFT

## How to use a date as the key shift?

The shift cipher can take a date as key (called date shift cipher ), generally in the formats YYYYMMDD is used as it contains a series of 8 digits which can be used as the shift key.

Example: DATECODE encrypted with the date 2020/10/10 or ( 2,0,2,0,1,0,1,0 ) becomes FAVEDOEE
