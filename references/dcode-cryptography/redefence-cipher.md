# Redefence Cipher

> Source: [https://www.dcode.fr/redefence-cipher](https://www.dcode.fr/redefence-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## How to encrypt using Redefence cipher?

The Redefence cipher is similar to the Rail-Fence transposition cipher except that it uses a key that defines both the number of levels in the zig zag and the order in which the lines are read.

Example: The plain message is DCODEZIGZAG and the key ZIG (of size N=3 letters).

The message is encrypted by Redefence (as with Rail Fence ) by writing it in zig-zag on N levels.

Example: (1-Z): D---E---Z-- (2-I): -C-D-Z-G-A- (3-G): --O---I---G

The characteristic of Redefence is to have a key that defines the reading order of the lines.

Example: The letters of the key ZIG are then arranged in alphabetical order G,I,Z which defines the reading order of the lines 3,2,1 .

Example: The encrypted message is therefore composed of line 3 OIG , line 2 CDZGA and line 1 DEZ so the final message is OIGCDZGADEZ

## How to decrypt a Redefence cipher?

Redefence decryption requires knowing the encryption key because it conditions the number of levels N and the order of reading.

Example: The encrypted message is DNRFEEEEC and the key ZAG (2,3,1) of size N=3.

The expected shape is drawn (depending on the number of levels and the length of the message).

Example: X---X---X -X-X-X-X- --X---X--

Then write the letters of the text starting with line 1 (defined according to the key).

Example: (2): R---F---E (3): -E-E-E-C- (1): --D---N--

The plain message is then readable in zig-zag from left to right.

Example: The plain text is REDEFENCE

## How to recognize Redefence ciphertext?

Redefence is a transposition cipher, so the frequency analysis and the coincidence index of the message are similar to that of the plaintext language.

## How to decipher Redefence without the key?

As for Rail-Fence , a brute-force attack of all levels (2 to N) is possible. Extra work is required to find the order of the lines.

## What are the variants of the Redefence cipher?

Redefence is a variant of the Rail Fence cipher adding the possibility of modifying the order of reading of the lines forming the zig-zag .
