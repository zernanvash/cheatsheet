# ROT-47 Cipher

> Source: [https://www.dcode.fr/rot-47-cipher](https://www.dcode.fr/rot-47-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is Rot-47? (Definition)

Rot-47 is a monoalphabetic substitution cipher based on a circular shift allowing the encoding of all visible ASCII characters (whereas a Rot13 cipher can only encrypt letters).

Rot47 uses a 94-character alphabet that is a subset of the ASCII table characters between the character 33 ! and the character 126 ~ .

## How to encrypt using Rot-47?

Rot47 encryption consists in replacing a character with another located 47 positions after in the alphabet . The conversion table to shift is: !"#$%& '()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNO PQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~

Example: DCODE is encrypted sr~st with ROT-47

The function is symmetrical, apply it twice to return to the original string: ROT47 ( ROT47 (A)))=A

## How to decrypt Rot-47 cipher?

The decryption of the Rot-47 is identical to the encryption because the substitution alphabet used is reversible. PQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~ !"#$%& '()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNO

Example: #@E\cf is decoded Rot-47

## Why the shift of 47?

The offset of 47 corresponds to half of the 94 printable ASCII characters. This choice ensures that the transformation is symmetrical: each character is exchanged with a single partner, making the operation involutive.

## How to recognize ROT-47 ciphertext?

The message uses ASCII characters and contains common letters as 6 or t which are the ciphered values of E and e .

Rot47 is a simple way to encode a message on discussion forums or social networks.

Sometimes the characters ! and ~ (exclamation point and tilde) are highlighted to serve as a clue [!-~] .

## What are the variants of the Rot-47 cipher?

Rot-47 is a variant of Rot13 generalized to all characters in the ASCII table , itself a variant of the Caesar cipher , a special case of shift cipher.

## What is the Linux command for the Rot-47?

It is possible to implement Rot-47 on the Linux command line using the tr tool, which allows character transliteration.

The following command performs the transformation: tr "P-~!-O" "!-~"
