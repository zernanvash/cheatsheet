# Swagman Cipher

> Source: [https://www.dcode.fr/swagman-cipher](https://www.dcode.fr/swagman-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is the Swagman cipher? (Definition)

The Swagman cipher is a transposition cipher based on a Latin square of size N. The key grid contains the numbers from 1 to N, without repetition in any row or column.

## How to encrypt a message with Swagman?

Choose a grid size N (usually between 4 and 8) and generate a Latin square containing the numbers from 1 to N, without repetition in any row or column.

Example: A Latin square of size N=4 1 3 2 4 3 4 1 2 2 1 4 3 4 2 3 1

1 3 2 4 3 4 1 2 2 1 4 3 4 2 3 1

The plaintext is then written horizontally into a table of N rows and padding letters, called nulls, are added if necessary to complete the table.

Example: Encrypt the message DCODESWAGMANCIPHER by writing it as D C O D E S W A G M A N C I P H E R X X

D C O D E S W A G M A N C I P H E R X X

For each column, perform a permutation of the letters: look at the numbers in the corresponding column of the key grid and read the letters according to the numerical order.

Example: The first column is 1,3,2,4 , so the letters are: D (row 1), A (row 3), S (row 2) and H (row 4), etc. The table becomes: D N A X E A E O G P S C R I M H W C D X

D N A X E A E O G P S C R I M H W C D X

The table is read column by column to form the final ciphertext (all column letter sequences are concatenated).

Example: The encrypted message is: DASHNECWAORCXGIDEPMX

## How to decrypt a message encrypted with Swagman?

Decrypting Swagman requires knowing the grid ( Latin square ).

Example: Decrypt DASHNECWAORCXGIDEPMX with the grid 1 3 2 4 3 4 1 2 2 1 4 3 4 2 3 1

1 3 2 4 3 4 1 2 2 1 4 3 4 2 3 1

— Determine the dimensions of the rectangle from the number of rows N in the grid. The number of columns is the length of the raw ciphertext divided by N.

Example: The square has size N=4, the message contains 20 letters, so the table has 5 columns.

— Reconstruct the table by copying the ciphertext column by column

Example: D N A X E A E O G P S C R I M H W C D X

D N A X E A E O G P S C R I M H W C D X

— For each column: use the key grid to recover the original row order and place the letters back into their correct positions.

Example: D C O D E S W A G M A N C I P H E R X X

D C O D E S W A G M A N C I P H E R X X

— Then read the table horizontally, row by row, to recover the plaintext.

## How to recognize a text encrypted with Swagman?

The Swagman cipher is a transposition cipher: the letters of the text are rearranged, but they are not replaced. The index of coincidence therefore remains identical to the plaintext (letter frequencies remain those of the original language).

The presence of a Latin square similar to a Sudoku grid is a clue.

## What to do if the key grid is unknown during decryption?

If the key grid is unknown, it is necessary to test different values of N, then attempt to reconstruct the text column by column.

To achieve this, it is possible to check whether the result contains plausible words or structures in the target language. A partially known plaintext can help reconstruct the grid.

## How to generate a valid key grid for Swagman?

A valid key grid for Swagman is a Latin square of size NxN. This means that each row and each column contains every number from 1 to N exactly once.

A simple way to generate a Latin square is to list the numbers in ascending order on the first row, then circularly shift them by 1 on each following row.

Example: 1 2 3 4 2 3 4 1 3 4 1 2 4 1 2 3

1 2 3 4 2 3 4 1 3 4 1 2 4 1 2 3

Any row or column permutation (such as swapping 2 or more rows or columns) preserves the property that the grid remains a Latin square .
