# Double Transposition Cipher

> Source: [https://www.dcode.fr/double-transposition-cipher](https://www.dcode.fr/double-transposition-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is a Double Transposition cipher? (Definition)

Double transposition encryption consists in the consecutive applications of 2 transposition ciphers. Generally, it is 2 columnar transposition using 2 distinct keys (but variations exist).

## How to encrypt using Double Transposition cipher?

The double transposition applies the simple transposition twice as the name suggests.

Example: Encrypt the message DCODE with the key KEY first, then the key WORD . The grid (1) is permuted a first time (2) (1) \ K E Y 1 D C O 2 D E (2) \ E K Y 1 C D O 2 E D

(1) \ K E Y 1 D C O 2 D E (2) \ E K Y 1 C D O 2 E D

\ K E Y 1 D C O 2 D E

\ E K Y 1 C D O 2 E D

The intermediate message is usually read in columns from bottom to top and then from left to right.

With the message found after the first permutation, then perform a second transposition with the key WORD . The ciphertext is also obtained by reading the grid by column (variations can apply).

Example: The encrypted intermediate message is CEDDO (3) and the final encrypted message is DEDCO (4): (3) \ W O R D 1 C E D D 2 O (4) \ D O R W 1 D E D C 2 ␣ ␣ ␣ O

(3) \ W O R D 1 C E D D 2 O (4) \ D O R W 1 D E D C 2 ␣ ␣ ␣ O

\ W O R D 1 C E D D 2 O

\ D O R W 1 D E D C 2 ␣ ␣ ␣ O

The encryption will be more robust if the lengths of the keys are coprime .

## How to decrypt Double Transposition cipher?

Double transposition decryption requires knowing the two permutation keys and the type of transposition for each (row or column)

Example: The crypted message is OECDDX has been transposed with 1 column transposition then with 1 line transposition with two identical keys: KEY .

The encrypted message must get two reversed transposition , in the opposite order of the original order, to get back the plain text.

Example: The grid (1) becomes after inverse permutation in rows (2) (1) \ 1 2 E O E K C D Y D X (2) \ 1 2 K C D E O E Y C X

(1) \ 1 2 E O E K C D Y D X (2) \ 1 2 K C D E O E Y C X

\ 1 2 E O E K C D Y D X

\ 1 2 K C D E O E Y C X

Example: The intermediate message CDOECX undergoes a second inverse permutation in columns (3) which gives the original starting grid (4) and the plain message DCODEX (3) E K Y C D O E D X (4) K E Y D C O D E X

(3) E K Y C D O E D X (4) K E Y D C O D E X

E K Y C D O E D X

K E Y D C O D E X

## How to recognize Double Transposition ciphertext?

A message encrypted by Double Transposition has a frequency analysis and a coincidence index normal.

The number of letters in the message is not a prime number.

## How to decipher Double Transposition without keys?

It is possible to find the key length by analyzing the prime decomposition of the text length .

By writing the text in the grid/checkerboard, permute the columns in order to find and recreate words on each rows, beginning with common bigrams (such as TH, HE, IN, etc.).

The lines should not follow each other, do not try to read words on several lines.

The second permutation is deductible from the line pieces that were created with the first permutation.

## What are the variants of the Double Transposition cipher?

It is possible to shuffle rows or columns in the desired order.

The UBCHI cipher inserts null letters between the 2 transpositions.

## When was Double Transposition invented?

The double transposition cipher has no date nor known author.
