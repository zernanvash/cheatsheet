# Monome-Dinome Cipher

> Source: [https://www.dcode.fr/monome-dinome-cipher](https://www.dcode.fr/monome-dinome-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is Monome-Dinome cipher? (Definition)

The monome-dinome cipher (or monome-binome ) is a substitution cipher according to the coordinates of a grid (from the family of the Polybius square ). Its characteristic is described in its name: certain letters are coded either by a monome (1 single digit) or by a dinome (2 digits).

## How to create a grid for Monome-Dinome?

Monome-Dinome is compatible with several types of deliberately incomplete grids with at least 2 special columns which will be used as the header name for the following rows.

— Variant 1: a 3x10 grid with 2 empty squares on the first row.

Example: Grid with the keys of rows 3 and 7: \ 0 1 2 3 4 5 6 7 8 9 A B C D E F G H 3 I J K L M N O P Q R 7 S T U V W X Y Z ␣ *

\ 0 1 2 3 4 5 6 7 8 9 A B C D E F G H 3 I J K L M N O P Q R 7 S T U V W X Y Z ␣ *

NB: 28 characters are possible, generally the 26 letters from A to Z, a space and a special character like *

— Variation 2: a 3x8 grid with missing columns.

Example: Grid with the keys of rows 3 and 7: \ 0 1 2 4 5 6 8 9 A B C D E F G H 3 I K L M N O P Q 7 R S T V W X Y Z

\ 0 1 2 4 5 6 8 9 A B C D E F G H 3 I K L M N O P Q 7 R S T V W X Y Z

NB: only 24 characters are possible, generally J is replaced by I and V replaced by U

## How to encrypt using Monome-Dinome cipher?

Monomial-binomial encryption consists in replacing each letter of the plain message by its coordinates in the grid.

Grid coordinates are read as [row,column]. The first row having no name, the coordinates are formed only from the name of the column.

Example: MONOME is coded 34,36,35,36,34,5 (3x10 grid)

## How to decrypt Monome-Dinome cipher?

Monome-binomial decryption consists of reading the numbers which are the coordinates of the letters in the grid.

Take the first digit N, if it is not a row number, then the plain letter is on the first row, column N. Otherwise, take the second digit M and the plain letter is row N, column M.

Example: 4303536345 splits 4,30,35,36,34,5 and translates to DINOME (3x10 grid)

## How to recognize a Monome-Dinome ciphertext? (Identification)

The text encoded by monome-binome is composed of digits.

The 2 digits representing key columns/rows are usually over-represented in frequency analysis .

## What are the variants of the Monome-Dinome cipher?

The grid can/must be generated from a keyword in order to obtain a disordered alphabet .

The order of the columns can also be modified from a keyword in order to make a permutation.

## When Monome-Dinome was invented?

The creation date of monome-binome is not known. There are historical traces of the use of this cipher during the Spanish Civil War in 1936.
