# Route/Path Cipher

> Source: [https://www.dcode.fr/route-cipher](https://www.dcode.fr/route-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is a route cipher? (Definition)

Route cipher is a way of writing a message using a transposition cipher. The idea is not to write the letters from left to right and top to bottom, like normal writing, but rather to follow a predefined path, like a serpentine in a grid, or in a zig zag way.

## How to encrypt using route cipher cipher?

Path-write encryption consists of writing the text in a grid/matrix and reading it using a road/path usually in switchbacks/coils/zigzags.

Example: The text DCODEROUTE , written horizontally on a 4x3 grid reads as a serpentine column DETERCOO..UD D↓ C↱ O⮧ D↑ E↓ R↑ O↓ U↑ T↳ E⮥ .↳ .⮥

D↓ C↱ O⮧ D↑ E↓ R↑ O↓ U↑ T↳ E⮥ .↳ .⮥

If the message does not fill the grid, add a character like . to end the column/row.

## How to decrypt a route cipher?

Decryption requires knowing the path (or at least the size of the grid) in order to write the letters of the message.

Example: The encrypted text PIN-AFD-THER on a grid of height 3 is written as P I N - A F D - T H E R

P I N - A F D - T H E R

Column reading according to the path returns the original text.

Example: The grid path reading returns PATHFINDER

## How to recognize route cipher text?

The message has a coincidence index similar to that of the plain language because it is a transposition .

The number of characters is a multiple of the width and height of the grid (and therefore can not be a prime number).

## How to decipher route cipher without the route?

The best method is to try different sizes and try to see if the beginning of the message is readable. dCode allows testing multiple possibilities automatically in order to detect the most probable.

## What are the variants of the route cipher?

On a grid of a given size, it is possible to write the text in the path of at least 8 (classical) ways (there are 2 possible directions for each of the 4 corners). Then reading can be a path too.

It is possible to imagine any type of path for letters, such as a spiral script. Another variant is Caesar box cipher.
