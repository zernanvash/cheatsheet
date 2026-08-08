# Collon Cipher

> Source: [https://www.dcode.fr/collon-cipher](https://www.dcode.fr/collon-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is the Collon cipher? (Definition)

The Colon cipher is a polygrammic (a letter is replaced by a bigram ) and polyalphabetic (the bigram can change) associated with a transposition . Using a grid, Collon 's cipher is similar to Polybius ' square, but whose coordinates are the letters of the grid.

## How to encrypt using Collon cipher?

Collon encryption uses a grid (usually 5x5) and requires a number N to separate the text into sets of N letters.

Example: Encrypt DCODE with series of N=2, ie DC/OD/E and the grid \ 1 2 3 4 5 1 A B C D E 2 F G H I K 3 L M N O P 4 Q R S T U 5 V W X Y Z

\ 1 2 3 4 5 1 A B C D E 2 F G H I K 3 L M N O P 4 Q R S T U 5 V W X Y Z

For each series of N characters, and for each letter in the series, start by locating the letter in the grid and note the letter at the beginning of the row and the letter at the bottom of the column.

Example: Letter Left of Row Bottom of column D A Y C A X

Letter Left of Row Bottom of column D A Y C A X

Once the series has been completed, write consecutively in the encrypted message the N rows headers and the N bottom of columns found.

Example: DCO is encrypted AA,YX The complete encrypted message is AAYXLAYYAZ .

## How to decrypt a Collon cipher?

Deciphering Collon requires knowledge of the grid and the number N.

Example: Decrypt AKKXZVKKKVZY , with N=3 and the grid \ 1 2 3 4 5 1 A B C D E 2 F G H I J 3 K L M N O 4 P Q R S T 5 U V X Y Z

\ 1 2 3 4 5 1 A B C D E 2 F G H I J 3 K L M N O 4 P Q R S T 5 U V X Y Z

Split the message into groups of size letters 2N then split each group into 2, to obtain 2 subgroups of N letters.

Example: AKKXZV,KKKVZY then AKK,XZV (for the first group)

Take the nth letters of each subgroup to get N bigrams

Example: AX,KZ,KV

For each bigram (L1,L2), locate the letter at the intersection of the row containing L1 and the column containing L2

Example: The letter at the intersection of the row containing A and the column containing X is the letter C (letter of the plain message)

Repeat the operation to find each letter of the plain message.

Example: The plain text is COLLON

## How to recognize a Collon ciphertext? (Cryptanalysis)

A Collon cipher message is:

— of even length

— composed of 9 distinct characters (at most)

— composed of blocks of N characters containing 5 distinct characters (at most)

## How to decipher Collon without the grid?

It is possible to find the letters forming the first column and the last row by testing all possible series lengths from 1 to n / 2 (or n = length of the ciphertext).

For each series length, it is possible to reconstitute the bigrams and to test their validity (9 maximum characters, 5 characters at the beginning and at the end, 1 single common character, etc.)

Thus, for lengths that do not conflict with the encryption rules, the letters of the first column and the last row can be deduced.

It is then possible to create a grid and attack the cryptogram as a simple substitution number.

Example: If the encryption grid consists of a keyword not interfering with the composition of the last row of the grid (less than 20 distinct letters), then the letters of the last row will follow the alphabetical order ( and will often be UVXYZ if the W is omitted).

If a bigram consists of a double letter (example AA ), then the plain letter corresponding to the encrypted bigram is the letter (example UU gives U ).

## What are the variants of the Collon cipher?

The cipher has several possible variants

— the use of other coordinates than the left of the row and the bottom of column (top of column, right/end of row, etc.)

— the reverse order of the coordinates, invert the coordinated letter of the row and the coordinated letter of the column

— the use of a variable N value (not available on dCode)
