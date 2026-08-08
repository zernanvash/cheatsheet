# Polybius Cipher

> Source: [https://www.dcode.fr/polybius-cipher](https://www.dcode.fr/polybius-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is the Polybius cipher? (Définition)

The Polybius cipher is a substitution cipher using a grid (the Polybius square ). Invented in ancient times by the Greek general Polybius , it transforms each letter into a pair of coordinates according to its position in the grid.

## How to encrypt using Polybius cipher?

The Polybius square cipher uses a 5x5 grid of letters with rows and columns marked with numerical coordinates from 1 to 5.

Example: \ 1 2 3 4 5 1 A B C D E 2 F G H I K 3 L M N O P 4 Q R S T U 5 V W X Y Z

\ 1 2 3 4 5 1 A B C D E 2 F G H I K 3 L M N O P 4 Q R S T U 5 V W X Y Z

— Associate each letter with a pair of numbers corresponding to its coordinates in the grid (row, column).

— Replace each letter of the plain text with its pair of numbers to obtain the encrypted message.

Example: Encode DCODE with the grid above: D is located in row 1 , column 4 , it is coded 14 ; C is located in row 1 , column 3 , it is coded 13 . The encrypted DCODE message is 14,13,34,14,15

## How to generate Polybius' square grid?

The grid is limited to 25 letters while the Latin alphabet has 26, so one letter must be omitted. Usually, I and J merge to fit in the 25 boxes, but sometimes it is U and V or even the Z that is omitted.

In addition , the position of the letters in the grid defines the encrypted message, it is recommended to mix the letters in the grid, one method is to use a password to generate a disordered alphabet that will be used to fill the grid.

In his original version, Polybius describes the grid with 24 characters of the Greek alphabet \ 1 2 3 4 5 1 A B Γ Δ E 2 Z H Θ I K 3 Λ M N Ξ O 4 Π P Σ T Y 5 Φ X Ψ Ω

\ 1 2 3 4 5 1 A B Γ Δ E 2 Z H Θ I K 3 Λ M N Ξ O 4 Π P Σ T Y 5 Φ X Ψ Ω

## How to decrypt Polybius cipher?

Polybius decryption requires to know the grid and consists in a substitution of couples of coordinates by the corresponding letter in the grid.

Example: The message to decrypt is 351332542114 with the grid (created with DCODE as key and without letter J ): \ 1 2 3 4 5 1 D C O E A 2 B F G H I 3 K L M N P 4 Q R S T U 5 V W X Y Z

\ 1 2 3 4 5 1 D C O E A 2 B F G H I 3 K L M N P 4 Q R S T U 5 V W X Y Z

Split the message in bigrams , couples of numbers that are the coordinates of each plain text letter.

Example: 35,13,32,54,21,14 , 35 stands for 3rd row, 5th column, so letter P , and so on. The plain message is POLYBE .

## How to recognize Polybius ciphertext?

The ciphered message is constituted of couples of coordinates (generally these are digits from 1 to 5) and so has an even number of characters (the possible pairs are: 11, 12, 13, 14, 15, 21, 22, 23, 24, 25, 31, 32, 33, 34, 35, 41, 42, 43, 44, 45, 51, 52, 53, 54, 55).

Coordinates may have at most 25 distinct values.

References to Greece ( Polybius comes from its author Πολύβιος / Polúbios in Greek) are a clue.

## How to decipher Polybius without the grid?

Polybius is a substitution by bigrams , replace each couple of coordinates by a random letter (there should be at most 25 distinct ones) and try a monoalphabetical substitution .

## What are the variants of the Polybius cipher?

Many variants have been created from the Polybius square .

It is possible to note the coordinates differently, for example with row or column names with characters other than the numbers 1 to 5, but also to reverse the row-column order by column-row.

It is possible to use a grid of a different size, not necessarily square, perhaps rectangular.

The author ( Polybius ) had proposed to transmit coded messages at a distance visually, for example, by means of torches. A method N in the right hand and M in the left hand for the pair N,M for example. This method is considered an ancestor of the telegraph.

Almost all encryption methods using grids can be considered as variants of the Polybius cipher .

The Nihilist cipher is a variant using an overciphering of the Polybius code.

## When was Polybius Cipher invented?

The greek historian Polybius described this method in 150 before JC in a work on military cryptography and communications systems.
