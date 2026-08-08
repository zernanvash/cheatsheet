# Delastelle Trifid Cipher

> Source: [https://www.dcode.fr/trifid-delastelle-cipher](https://www.dcode.fr/trifid-delastelle-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is Delastelle Trifid cipher? (Definition)

Delatelle trifid cipher is a polyalphabetic cipher using a three-dimensional grid (or 3 grids) and triplets (grid, row, column).

## How to encrypt using Delastelle Trifid cipher?

The Delastelle trifid cipher uses three 9-character grids (for 27 distinct characters in total) and an integer N (usually 5 or 7).

Example: Encrypt the message SECRET , with N = 5 and grids Grid 1 Grid 2 Grid 3 \ 1 2 3 1 A B C 2 D E F 3 G H I \ 1 2 3 1 J K L 2 M N O 3 P Q R \ 1 2 3 1 S T U 2 V W X 3 Y Z _

Grid 1 Grid 2 Grid 3 \ 1 2 3 1 A B C 2 D E F 3 G H I \ 1 2 3 1 J K L 2 M N O 3 P Q R \ 1 2 3 1 S T U 2 V W X 3 Y Z _

\ 1 2 3 1 A B C 2 D E F 3 G H I

\ 1 2 3 1 J K L 2 M N O 3 P Q R

\ 1 2 3 1 S T U 2 V W X 3 Y Z _

Often, a keyword is used to generate a disordered alphabet with 27 characters (the Latin alphabet accompanied by another symbol like _ replacing any non-alphabetic character)

Step 1: For each character, search for it in grids and note are triplet of 3 corresponding digits (grid, row, column)

Example: S is in grid 3 , row 1 , column 1 , its triplet is 311

Step 2: Write the triplets in columns, in groups of N columns next to each other and read each group in rows.

Example: S E C R E | T 3 1 1 2 1 3 1 2 1 3 2 1 1 2 3 3 2 2

S E C R E | T 3 1 1 2 1 3 1 2 1 3 2 1 1 2 3 3 2 2

Reading group 1: 31121,12132,12332 , group 2: 312

Step 3: Cut out each sequence of digits read in triplet (group of 3 digits) corresponding to [grid, row, column]and note the corresponding letter. These letters constitute the encrypted message.

Example: 311,211,213,212,332,312 corresponds to SJLKZT

## How to decrypt Delastelle Trifid cipher?

Decryption is very similar to encryption, the difference is in step 2.

Example: Decrypt the message SJLKZT , with N = 5 and grids Grid 1 Grid 2 Grid 3 \ 1 2 3 1 A B C 2 D E F 3 G H I \ 1 2 3 1 J K L 2 M N O 3 P Q R \ 1 2 3 1 S T U 2 V W X 3 Y Z _

Grid 1 Grid 2 Grid 3 \ 1 2 3 1 A B C 2 D E F 3 G H I \ 1 2 3 1 J K L 2 M N O 3 P Q R \ 1 2 3 1 S T U 2 V W X 3 Y Z _

\ 1 2 3 1 A B C 2 D E F 3 G H I

\ 1 2 3 1 J K L 2 M N O 3 P Q R

\ 1 2 3 1 S T U 2 V W X 3 Y Z _

Step 1: identical to encryption

Step 2: Take the triplets in groups of N and write them in N-length rows below each other then read each group in columns.

Example: 311,211,213,212,332,312 is written 3 1 1 2 1 | 3 1 2 1 2 1 3 2 | 1 2 3 3 3 |

3 1 1 2 1 | 3 1 2 1 2 1 3 2 | 1 2 3 3 3 |

Reading group 1: 311,122,113,233,123 , group 2: 3,1,2

Step 3: Identical to encryption

Example: 311,122,113,233,123,312 corresponds to the plain message SECRET

## How to recognize a Trifid ciphertext?

The message is theoretically composed of not more than 27 distinct characters.

## What are the variants of the Trifid cipher?

The N number quickly changes the encrypted message, for better encryption, it is advisable to take a value of N coprime with 3.

## When was Trifid invented?

Félix Marie Delastelle described this encryption in 1902 in his book Traité Élémentaire de Cryptographie
