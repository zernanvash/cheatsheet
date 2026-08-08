# Two-square Cipher

> Source: [https://www.dcode.fr/two-square-cipher](https://www.dcode.fr/two-square-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is the Two-Square cipher? (Definition)

Two-square cipher is a polygrammic cipher that uses a playfair -like process to encrypt (it is also called double playfair ), except that it uses two keys or 5x5 square-grids

## How to encrypt using Two-Square cipher?

Two-Square cipher (or double square cipher) encryption uses two squared grid/checkboard placed side to side (default horizontal variant), or one above the other (vertical variant), sometimes generated with a key word ( deranged alphabet )

Example: Crypt DCODE with two grids (horizontal) generated with the words KEY and WORD respectively \ 1 2 3 4 5 1 K E Y A B 2 C D F G H 3 I L M N O 4 P Q R S T 5 U V W X Z \ 1 2 3 4 5 1 W O R D A 2 B C E F G 3 H I K L M 4 N P Q S T 5 U V X Y Z

\ 1 2 3 4 5 1 K E Y A B 2 C D F G H 3 I L M N O 4 P Q R S T 5 U V W X Z \ 1 2 3 4 5 1 W O R D A 2 B C E F G 3 H I K L M 4 N P Q S T 5 U V X Y Z

\ 1 2 3 4 5 1 K E Y A B 2 C D F G H 3 I L M N O 4 P Q R S T 5 U V W X Z

\ 1 2 3 4 5 1 W O R D A 2 B C E F G 3 H I K L M 4 N P Q S T 5 U V X Y Z

The first step consists in splitting the plain text into bigrams (couples of two letters). If the last bigram is incomplete (odd message length), add a random letter from the grid to complete the bigram .

Example: DC , OD , EZ (letter Z added)

Second step, for each bigram , find the first letter in the first grid and the second letter in the second grid and apply the following rules:

— if the letters are on the same line (or columns in vertical version), reverse them

— else, replace them by the letters one the same rows but on the opposite corner of an imaginary rectangle, with the two first letters as opposite vertices. In practice, locate the two original letters and find the two other letters that create an imaginary rectangle. Encrypted letters are written beginning with the one on the same row (horizontal variant) as the first letter of the plain bigram (use same column with vertical variant)

Example: D (grid 1) and C (grid 2) are on the same row, switch them: CD O (grid 1, row 3, column 5) and D (grid 2, row 1, column 4) are not on the same row, opposite corners are L (grid 2, row 3, column 4) and B (grid 1, row 1, column 5) E (grid 1, row 1, column 2) and Z (grid 2, row 5, column 5) are not on the same row, opposite corners are A (grid 2, row 1, column 5) and V (grid 1, row 5, column 2) Final encrypted text is then CDLBAV

## How to decrypt a Two-Square cipher?

Two-Square cipher Decryption requires two grids/checkboards generated with two keys. The cipher text is split into bigrams (couples of 2 letters).

Example: The cipher text is CDLBAV (split in CD , LB , AV ) and the grids are in horizontal position \ 1 2 3 4 5 1 K E Y A B 2 C D F G H 3 I L M N O 4 P Q R S T 5 U V W X Z \ 1 2 3 4 5 1 W O R D A 2 B C E F G 3 H I K L M 4 N P Q S T 5 U V X Y Z

\ 1 2 3 4 5 1 K E Y A B 2 C D F G H 3 I L M N O 4 P Q R S T 5 U V W X Z \ 1 2 3 4 5 1 W O R D A 2 B C E F G 3 H I K L M 4 N P Q S T 5 U V X Y Z

\ 1 2 3 4 5 1 K E Y A B 2 C D F G H 3 I L M N O 4 P Q R S T 5 U V W X Z

\ 1 2 3 4 5 1 W O R D A 2 B C E F G 3 H I K L M 4 N P Q S T 5 U V X Y Z

For each bigram , locate the first letter in grid 2 and the second letter in grid 1.

If the two letters are on the same row (or column in vertical version), swap them.

Else, find the 2 original letters by locating the two letters that complete the imaginary rectangle (see encryption). As for the encryption process, write the letters by starting with the same row (or column depending on the variant used) as the first letter of the encrypted bigram .

Example: C (grid 2) and D (grid 1) are on the same row, switch them: DC L (grid 2, row 3, column 4) and B (grid 1, row 1, column 5) are not on the same row, opposite corners are O (grid 1, row 3, column 5) and D (grid 2, row 1, column 4) A (grid 2, row 1, column 5) and V (grid 1, row 5, column 2) are not on the same row, opposite corners are E (grid 1, row 1, column 2) and Z (grid 2, row 5, column 5) The original plain text is DCODEZ .

## How to recognize Two-Square ciphertext?

The ciphered message needs 2 keys, and generally has a maximum of 25 distinct characters.

The presence of 2 grids or 2 squares is a clue.

All references to pairs of words or famous duos (used as keys for generating the grids) are clues.

## How to decipher Two-Square without the two squares?

Two-Square can be cracked by a frequency analysis of bigrams if the text is long enough.

dCode offers a brute force grid attack.

## What are the variants of the Two-Square cipher?

Excepting variations due to creating a deranged alphabet out of the keys, it is possible to modify:

— the position of the grids, for example, by setting them vertically rather than horizontally. In this case, encryption and decryption processes should take into account bigram letters on the same column rather than on the same row

— the order of the letters of the bigrams (by default, the first letter comes from grid 2 then grid 1)

— the order of the grid (swap grid 1 and 2)

## When was Two-Square invented?

Probably near of the invention of the PlayFair algorithm (towards 1850)
