# Transposition Cipher

> Source: [https://www.dcode.fr/transposition-cipher](https://www.dcode.fr/transposition-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is the Transposition Cipher? (Definition)

Transposition cipher is an encryption method that rearranges the characters in a message into another order/arrangement defined by a transposition key (or permutation key).

Transposition cipher is the generic name given to any encryption that involves rearranging the letters of plain text into a new order. However, in the literature, the term transposition cipher is generally associated with a subset: columnar transposition (or rectangular transposition ) which consists of writing the plain message in a table / grid / rectangle, then arranging the columns of this table according to a defined permutation.

## What is a transposition key?

The transposition/permutation key is a series of numbers (often generated from a word) which indicates in which order to arrange the letters.

Example: The word KEY makes the permutation 2,1,3 : Before alphabetical sort After alphabetical sort Word K,E,Y E,K,Y Column Order 1,2,3 2,1,3

Before alphabetical sort After alphabetical sort Word K,E,Y E,K,Y Column Order 1,2,3 2,1,3

## How to encrypt using a Transposition cipher?

The columnar transposition cipher consists to write a message in a table of width N (with N, the size of the permutation), row by row (or column by column), to permute the columns according to the order of the key and read the result in columns (or by rows).

Example: Encrypt MESSAGE by columnar transposition with the key CODE (permutation 1,3,4,2 ) gives MASESEG (writing in rows and reading the table by columns) Columns 1,2,3,4 Sorted cols 1,3,4,2 Plain text M,E,S,S Cipher text M,S,S,E A,G,E,_ A,E,_,G

Columns 1,2,3,4 Sorted cols 1,3,4,2 Plain text M,E,S,S Cipher text M,S,S,E A,G,E,_ A,E,_,G

Some variants consist in reading the table in rows and not in columns, in this case, the encrypted message with a reading in column would be MASES_EG .

If the grid contains empty boxes, it is possible to complete them with a neutral letter X (or other more frequent letter) in order to facilitate manual decryption.

## How to decrypt with a transposition cipher?

Transposition cipher decryption is identical to encryption except that the order of the columns is changed/reversed.

If the message has a length (number of characters) which is not a multiple of the size of the permutation, then it is necessary to pre-calculate the position of the empty boxes in the grid (by simulating a filling similar to encryption).

Example: A permutation 2,1,3 has been used to get the message CDOEDX (read by row): Columns 2,1,3 Sorted columns 1,2,3 Ciphertext C,D,O Plaintext D,C,O E,D,X D,E,X

Columns 2,1,3 Sorted columns 1,2,3 Ciphertext C,D,O Plaintext D,C,O E,D,X D,E,X

Example: The plain text is DCODEX .

If the message was read in columns, first write the table by columns

Example: A permutation 2,1,3 has been used to get the message CEDDOX (read by column): Columns 2,1,3 Sorted columns 1,2,3 Ciphertext C,D,O Plaintext D,C,O E,D,X D,E,X

Columns 2,1,3 Sorted columns 1,2,3 Ciphertext C,D,O Plaintext D,C,O E,D,X D,E,X

Example: The plain text is DCODEX .

## How to recognize a transposition ciphertext?

The message consists of the letters of the original message but in a different order (rearrangement of characters in disorder).

The index of coincidence is identical to that of the one of the language of the plaintext.

The bigram index of coincidenceis, on the other hand, different.

## How to decipher a transposition cipher without key?

It is possible to test all the permutations if the key is not too long, but the most effective method is to have or try to guess a word from the plain text and to deduce the permutations of the columns.

If the encrypted message is composed of very few words (1, 2 or 3) then an anagram solver can make it possible to find them.

## What are the variants of the transposition cipher?

The transposition cipher is, along with the substitution cipher, one of the most used bricks for more elaborate ciphers. There are dozens of ciphers that use it like ADFGVX , Amsco , Double Transposition , Redefence , etc.

## Why completing the empty cells of the transposition table?

The empty squares of the grid introduce an additional difficulty, rather time-consuming, when deciphering. Because the receiver of the message must calculate the position of these, which requires among other things, to count the number of characters of the message. If the empty boxes are not completed and the pre-calculation is not done, errors could appear in the reorganization of certain letters (especially the last ones).
