# Wolseley Cipher

> Source: [https://www.dcode.fr/wolseley-cipher](https://www.dcode.fr/wolseley-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## How to encrypt using Wolseley cipher?

The Wolseley cipher is a reversible substitution cipher whose substitution alphabet is based on a key generated with deranged alphabet .

In its original version, the alphabet has only 25 letters to fit in a 5x5 grid.

Example: The keyword SECRET allows to generate the alphabet SECRTABDFGHIKLMNOPQUVWXYZ (the J has been omitted to keep only 25 letters)

Encryption consists of substituting each letter in position n in the alphabet by the letter in position n but starting from the end of the alphabet. If the alphabet has only 25 letters, then the letter in position n is substituted by the letter in position 25-n (starting from 0).

Example: Plain letter SECRTABDFGHIKLMNOPQUVWXYZ Cipher letter ZYXWVUQPONMLKIHGFDBATRCES Plain message WOLSELEY Cipher message RFIZYIYE

Plain letter SECRTABDFGHIKLMNOPQUVWXYZ Cipher letter ZYXWVUQPONMLKIHGFDBATRCES Plain message WOLSELEY Cipher message RFIZYIYE

## How to decrypt Wolseley cipher?

Decryption is identical to encryption because the substitution table reversible (a double encrypted letter goes back to the initial letter)

To simplify handwriting, Wolseley proposed writing the alphabet as a grid: \ 1 2 3 4 5 1 S E C R T 2 A B D F G 3 H I K L M 4 N O P Q U 5 V W X Y Z thus the plain letter and the cipherletter are diametrically opposed to the letter in the center of the grid (which is the only invariant letter).

\ 1 2 3 4 5 1 S E C R T 2 A B D F G 3 H I K L M 4 N O P Q U 5 V W X Y Z

## How to recognize a Wolseley ciphertext?

The Wolseley number is a substitution code

— The coincidence index of the encrypted message is identical to that of the plain message

— In its original version, the code has only 25 distinct letters

## How to decipher Wolseley without key?

Frequency analysis and the dCode monoalphabetic substitution tool allow to find the plain message without much difficulty or at least to position the current letters such as the letter E .

## What are the variants of the Wolseley cipher?

Without a keyword, the Wolseley code is identical to the Atbash cipher (with 26 letters).

## When Wolseley have been invented?

Lord commander Garnet Joseph Wolseley used this code in the 18th century (although it bears his name today, the inventor of this cipher is unknown).
