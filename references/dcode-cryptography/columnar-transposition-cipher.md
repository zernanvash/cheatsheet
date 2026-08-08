# Columnar Transposition Cipher

> Source: [https://www.dcode.fr/columnar-transposition-cipher](https://www.dcode.fr/columnar-transposition-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is a Columnar Transposition cipher? (Definition)

A columnar transposition cipher is an encryption method that swaps the columns of a table (or a grid) containing the plain message to obtain an encrypted message.

## How to encrypt using a Columnar Transposition cipher?

Column transposition encryption writes plaintext in a rectangular array of N columns (inline fill) with N the size of the permutation key.

Example: The text COLUMNS is encrypted with the permutation 1,3,2 of the key word COL , it is written in the table Columns 1,2,3 Permuted cols 1,3,2 Plaintext C,O,L Ciphertext C,L,O U,M,N U,N,M S,X,X S,X,X

Columns 1,2,3 Permuted cols 1,3,2 Plaintext C,O,L Ciphertext C,L,O U,M,N U,N,M S,X,X S,X,X

Fill in the empty boxes with a neutral letter (like X ).

The encrypted message is then read in columns

Example: CUSLNXOMX

It is possible to read line by line, in which case the encrypted message would be CLOUNMSXX

## How to decrypt with a Columnar Transposition cipher?

Decryption by Columnar Transposition is similar to encryption. The difference lies in the writing in the table (in row or in column according to the reading method used during the encryption), as well as in the order of the columns which are permuted before being sorted again in ascending order.

Example: A permutation 1,3,2 was used to obtain the message CUSLNXOMX (reading by columns): Permuted cols 1,3,2 Sorted cols 1,2,3 Ciphertext C,L,O Plaintext C,O,L U,N,M U,M,N S,X,X S,X,X

Permuted cols 1,3,2 Sorted cols 1,2,3 Ciphertext C,L,O Plaintext C,O,L U,N,M U,M,N S,X,X S,X,X

## How to recognize a Columnar Transposition ciphertext?

The message consists of the transposed / swapped letters, so it has all the letters of the original message but in a different order.

The coincidence index after transposition of columns is unchanged from that of the plain text language.

## How to decipher a Columnar Transposition without the key?

For short permutations (up to 5-6 letters), a brute-force algorithm can test all permutations.

Otherwise, by knowing a word of the plain text (if possible with unusual letters), it is possible to find the position of its letters and to deduce the compatible columns permutations.
