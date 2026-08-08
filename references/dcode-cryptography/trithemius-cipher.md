# Trithemius Cipher

> Source: [https://www.dcode.fr/trithemius-cipher](https://www.dcode.fr/trithemius-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is the Trithemius cipher? (Definition)

The Trithemian cipher, also known as the Trithemian cipher , is an encryption method based on the principle of substitution according to successive shifts.

## How to encrypt using Trithemius cipher?

The Trithemius code is a successive shift cipher, using positive and ascending (ie. to the right) shifts in the alphabet from 0 to N where N is the length of the text. If the end of the alphabet is reached, start from the beginning.

Example: To code DCODE shift D from +0 an get D , shift C by +1 and get D , shift O by +2 and get Q , shift D by +3 and get G , and shift E by +4 and get I . The coded message is DDQGI .

Another method, more visual, consists of using the following grid, selecting the column whose name is the plain letter at the top, and for row the number of the letter on the right (arrived at 27, start again at 1), the intersection is the encrypted letter.

## How to decrypt Trithemius cipher?

Trithemius decryption requires successively shifting in the other direction in the alphabet: shifting $ N $ to the left (or negatively to the right, adding $ -N $).

Example: To decode TSKWLJSPCB shift T by 0 and get T , shift S by -1 and get R , shift K by -2 and get I , etc. The plain message is TRITHEMIUS .

## What are the variants of the trithemius cipher?

— The shift may be ascending/increasing or descending/decreasing.

— By default, the offset starts at 0, but it is conceivable to start it at 1 or any other number.

— The alphabet used can be a deranged alphabet or a completely personalized alphabet.

— Other types of shift sequences may be imagined (see shift ciphers).

With a classical alphabet ABCDEFGHIJKLMNOPQRSTUVWXYZ , Trithemius cipher is equivalent to a Vigenere cipher with ABCDEFGHIJKLMNOPQRSTUVWXYZ .

Trithemius cipher is a variant to a Caesar cipher with a shift that increases by 1 by each letter starting at 0.

## How to recognize Trithemius ciphertext?

The ciphered message has a low index of coincidence (0.04-0.05).

A Vigenère -like key length analysis will return a likely size of 26.

## When Trithemius was invented?

Trithème (a German abbot) would have described it during the Renaissance, around 1480.
