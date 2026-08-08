# Bifid Cipher

> Source: [https://www.dcode.fr/bifid-cipher](https://www.dcode.fr/bifid-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is the Bifid cipher? (Definition)

The bifid cipher is a polygraphic cipher invented by Felix Delastelle that combines a substitution using a Polybius square and a transposition . Its principle is based on the fractionation of letters into coordinates (row, column), followed by a shuffling of these coordinates before reconstituting the ciphered letters.

## How to encrypt using Bifid cipher?

Bifid ciphers require a square grid (possibly generated from a keyword, typically 5x5) and a period N corresponding to the block size.

If N = 1, the cipher has no effect: each letter is simply replaced by itself after transformation. Therefore, it is recommended to use a value of 2 or higher.

Example: Encrypt the plain message DCODE with the grid (generated with the word SECRET ): \ 1 2 3 4 5 1 S E C R T 2 A B D F G 3 H I K L M 4 N O P Q U 5 V W X Y Z

\ 1 2 3 4 5 1 S E C R T 2 A B D F G 3 H I K L M 4 N O P Q U 5 V W X Y Z

— Choose a block size N and group the letters into blocks of size N.

Example: A period of length N=3 for DCODE gives DCO,DE (no need to complete the block if the last one is not of length N)

This text-splitting is not mandatory, but simplifies encryption/decryption for long texts. For a non split encryption, imagine a period size of N=1 (or a period size equal to or greater than the number of letters in the plain message)

— For each letter of the block, write the coordinates of the letters (row, column) in a table.

Example: Take the first block DCO . D=(2,3) , C=(1,3) , O=(4,2) and write it in a table: D 2 3 C 1 3 O 4 2

D 2 3 C 1 3 O 4 2

— To get new coordinates, read the numbers of the table vertically by columns.

Example: The vertical reading gives 2,1,4,3,3,2 or the coordinates (2,1),(4,3),(3,2) .

— Replace the coordinates with the corresponding letters in the grid.

Example: (2,1) for A , (4,3) for P and (3,2) for I .

These steps are repeated for each block.

Example: The final encrypted message is APIAI

## How to decrypt a Bifid cipher?

Bifid decryption begins identically to encryption.

Example: The message DBAKS has been encrypted with a period N=3 and the grid (generated with the word MESSAGE ): \ 1 2 3 4 5 1 M E S A G 2 B C D F H 3 I K L N O 4 P Q R T U 5 V W X Y Z

\ 1 2 3 4 5 1 M E S A G 2 B C D F H 3 I K L N O 4 P Q R T U 5 V W X Y Z

The message is split into period/block of size N

Example: The message is decomposed in block of 3: DBA,KS

Convert each letter into coordinates (row, column)

Example: The letters of the block D,B,A have the respective coordinates (2,3),(2,1),(1,4) .

Write the coordinates on 2 rows (and therefore N columns, except possibly for the last group)

Example: 2 3 2 1 1 4

2 3 2 1 1 4

Then, read vertically by columns

Example: You get 2,1,3,1,2,4 or (2,1),(3,1),(2,4) .

The new coordinates are then associated with the corresponding letters in the grid.

Example: You find the plain letters (2,1)=B , (3,1)=I and (2,4)=F

These steps are repeated for each block.

Example: The plaintext message is BIFID .

## How to recognize Bifid ciphertext?

The message has a low coincidence index around 0.04 to 0.05.

If the grid is 5x5 then it can have at most 25 distinct characters.

## What does bifid mean?

Bifid means 'divided into two parts'. In this cipher, the coordinates of the letters are separated into two sequences (rows and columns), then recombined, which constitutes the core of the process.

## Why should the period not be N=1?

With a period of N=1, each block contains only one letter. Therefore, the coordinates are never mixed with those of other letters.

Therefore, there is neither diffusion nor transposition : the text remains unchanged after encryption. Using N=1 is equivalent to disabling encryption.

## Why are odd periods preferable to even periods?

Even periods can introduce exploitable regularities for cryptographic analysis.

When N is even, the separation of coordinates produces two halves of equal size, which can preserve some correlations between initial and final positions. This facilitates attacks based on the cipher's structure, particularly those that search for alignments or repeating patterns.

With an odd period, this symmetry is broken, which tends to shuffle the coordinates more effectively and reduce exploitable correlations.

However, this difference remains subtle: overall security depends primarily on the size of N and the length of the message.

## When was the Bifid cipher invented?

Felix-Marie Delastelle described the bifid cipher in 1902 in his work 'Traité Élémentaire de Cryptographie'.
