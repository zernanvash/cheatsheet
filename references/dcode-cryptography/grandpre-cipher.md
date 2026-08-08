# Grandpré Cipher

> Source: [https://www.dcode.fr/grandpre-cipher](https://www.dcode.fr/grandpre-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is the Grandpré cipher? (Definition)

The Grandpré cipher is a homophonic substitution cipher (the same letter can have several encryption) using a 10x10 grid.

The author ( Grandpré ) calls his process Méthode de Carré 10x10 (10x10 Square Method)

## How to encrypt using Grandpré cipher?

Encryption requires a grid, in the original version described by Grandpré , it is 10x10 in size and consists of 10 words (one per line) and the initials of the first 10 words themselves constitute an 11th word. Row and column coordinates are numbered 1,2,3,4,5,6,7,8,9,0.

Example: Grandpré proposes as a grid (which he calls checkerboard ) \ 1 2 3 4 5 6 7 8 9 0 1 V O L U P T U E U X 2 I N Q U I E T U D E 3 M A J E S T U E U X 4 O B L I G E A N C E 5 U N I F O R M I T E 6 T W I C K E N H A M 7 I N G O L S T A D T 8 E I N S I E D E L N 9 R Y M K I E W I C Z 0 S H R E W S B U R Y

\ 1 2 3 4 5 6 7 8 9 0 1 V O L U P T U E U X 2 I N Q U I E T U D E 3 M A J E S T U E U X 4 O B L I G E A N C E 5 U N I F O R M I T E 6 T W I C K E N H A M 7 I N G O L S T A D T 8 E I N S I E D E L N 9 R Y M K I E W I C Z 0 S H R E W S B U R Y

The encrypted message consists of the substitution of the letters of the clear message by their coordinates (line, column) in the grid (if there are several, take one randomly).

Example: GRANDPRE can be coded 73 09 78 22 29 15 03 88

## How to decrypt Grandpré cipher?

Grandpré decryption requires knowledge of the encryption grid (or of the 10 words composing it). The method consists of taking the digits of the code in pairs, the first digit indicating the row and the second the column of the letter in the grid.

Example: 45 56 32 72 29 15 03 66 is decrypted GRANDPRE

## How to recognize a Grandpré ciphertext? (Identification)

A message encrypted by Grandpré consists of digits, arranged in pairs of 2, so has an even length.

The presence of 10 10-letter words can be a clue.

## What are the variants of the Grandpré cipher?

Grandpré 's method has evolved and some (including the American Cryptogram Association) recommend 8x8 size squares.

It is also possible to use column numbering starting from 0.

Polybius square is a very similar cipher method, but with a 5x5 square and no repeating letters in the grid.

## What are Grandpré checkerboards?

Grandpré presents 7 grids/checkerboards (called damier ) to present its encryption process:

Damier 1 : VOLUPTUEUX INQUIETUDE MAJESTUEUX OBLIGEANCE UNIFORMITE TWICKENHAM INGOLSTADT EINSIEDELN RYMKIEWICZ SHREWSBURY

Damier 1 : VOLUPTUEUX INQUIETUDE MAJESTUEUX OBLIGEANCE UNIFORMITE TWICKENHAM INGOLSTADT EINSIEDELN RYMKIEWICZ SHREWSBURY

Damier 2 : INVENTAIRE NIEMCEWICZ JACQUEMART UNIFORMITE SCHLESTADT TYPOGRAPHE INTERLAKEN CHRYSALIDE EXHALAISON SEBASTOPOL

Damier 3 : NEVROTOMIE EQUATORIAL UNIVERSITE FRAUDULEUX CHAMPIGNON HAWKESBURY AJUSTEMENT TREBIZONDE ELLIPSOIDE LOGARITHME

Damier 4 : JUXTAPOSER AUSTERLITZ CARTWRIGHT QUILLEBEUF UNIVERSITE ELNSIEDELN MADAGASCAR APOCALYPSE ROUTSCHOUK DOUARNENEZ

Damier 5 : HERCULANUM ANTIQUAIRE WURTZBOURG KLAGENFURT EXHUMATION SUPERLATIF BIJOUTERIE UNIVERSITE ROTHSCHILD YSSINGEAUX

Damier 6 : BRUXELLOIS INDULGENCE VALPARAISO ORPHELINAT UNIVERSITE ABJURATION QUEENSTOWN UNIFORMITE EINSIEDELN RYMKIEWICZ

Damier 7 : LOGARITHME ASSUJETTIR BENEFICIER YSSINGEAUX RAPSODISTE INTERLAKEN NIEMCEWICZ TRAVAILLER HERCULANUM EQUATORIAL

It also features a long list of 10-letter words (in French).

## When was Grandpré cipher invented?

A. de Grandpré described his process in 1905 in his book, a cryptographic treatise, entitled Cryptographie pratique (Practical Cryptography) .
