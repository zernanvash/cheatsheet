# Phillips Cipher

> Source: [https://www.dcode.fr/phillips-cipher](https://www.dcode.fr/phillips-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is the Phillips cipher? (Definition)

The Philips cipher is a polyalphabetic substitution cipher by blocks using 8 grids (1 initial grid and 7 others created from the first).

## How to encrypt using Phillips cipher?

Philips Encryption uses an initial grid of 5x5 (or keyword to generate the grid).

Example: Basic Grid (with Z omitted) \ 1 2 3 4 5 1 A B C D E 2 F G H I J 3 K L M N O 4 P Q R S T 5 U V W X Y

\ 1 2 3 4 5 1 A B C D E 2 F G H I J 3 K L M N O 4 P Q R S T 5 U V W X Y

The first step is to generate 7 other 5x5 grids of letters (to obtain 8 grids in total). The grid 1 is the initial grid, the grids 2, 3, 4 and 5 are obtained from the grid 1 by swapping line 1 with lines 2, 3, 4 and 5 respectively, and finally the grids 6, 7 and 8 are obtained from the grid 5 by switching line 1 with the line respectively 2, 3 and 4.

Example: Grid 1 \ 1 2 3 4 5 1 A B C D E 2 F G H I J 3 K L M N O 4 P Q R S T 5 U V W X Y Grid 2 \ 1 2 3 4 5 1 F G H I J 2 A B C D E 3 - - - - - 4 - - - - - 5 - - - - - Grid 3 \ 1 2 3 4 5 1 K L M N O 2 - - - - - 3 A B C D E 4 - - - - - 5 - - - - - Grid 4 \ 1 2 3 4 5 1 P Q R S T 2 - - - - - 3 - - - - - 4 A B C D E 5 - - - - - Grid 5 \ 1 2 3 4 5 1 U V W X Y 2 F G H I J 3 K L M N O 4 P Q R S T 5 A B C D E Grid 6 \ 1 2 3 4 5 1 F G H I J 2 U V W X Y 3 - - - - - 4 - - - - - 5 A B C D E Grid 7 \ 1 2 3 4 5 1 K L M N O 2 - - - - - 3 U V W X Y 4 - - - - - 5 A B C D E Grid 8 \ 1 2 3 4 5 1 P Q R S T 2 - - - - - 3 - - - - - 4 U V W X Y 5 A B C D E

Grid 1 \ 1 2 3 4 5 1 A B C D E 2 F G H I J 3 K L M N O 4 P Q R S T 5 U V W X Y Grid 2 \ 1 2 3 4 5 1 F G H I J 2 A B C D E 3 - - - - - 4 - - - - - 5 - - - - - Grid 3 \ 1 2 3 4 5 1 K L M N O 2 - - - - - 3 A B C D E 4 - - - - - 5 - - - - - Grid 4 \ 1 2 3 4 5 1 P Q R S T 2 - - - - - 3 - - - - - 4 A B C D E 5 - - - - - Grid 5 \ 1 2 3 4 5 1 U V W X Y 2 F G H I J 3 K L M N O 4 P Q R S T 5 A B C D E Grid 6 \ 1 2 3 4 5 1 F G H I J 2 U V W X Y 3 - - - - - 4 - - - - - 5 A B C D E Grid 7 \ 1 2 3 4 5 1 K L M N O 2 - - - - - 3 U V W X Y 4 - - - - - 5 A B C D E Grid 8 \ 1 2 3 4 5 1 P Q R S T 2 - - - - - 3 - - - - - 4 U V W X Y 5 A B C D E

\ 1 2 3 4 5 1 A B C D E 2 F G H I J 3 K L M N O 4 P Q R S T 5 U V W X Y

\ 1 2 3 4 5 1 F G H I J 2 A B C D E 3 - - - - - 4 - - - - - 5 - - - - -

\ 1 2 3 4 5 1 K L M N O 2 - - - - - 3 A B C D E 4 - - - - - 5 - - - - -

\ 1 2 3 4 5 1 P Q R S T 2 - - - - - 3 - - - - - 4 A B C D E 5 - - - - -

\ 1 2 3 4 5 1 U V W X Y 2 F G H I J 3 K L M N O 4 P Q R S T 5 A B C D E

\ 1 2 3 4 5 1 F G H I J 2 U V W X Y 3 - - - - - 4 - - - - - 5 A B C D E

\ 1 2 3 4 5 1 K L M N O 2 - - - - - 3 U V W X Y 4 - - - - - 5 A B C D E

\ 1 2 3 4 5 1 P Q R S T 2 - - - - - 3 - - - - - 4 U V W X Y 5 A B C D E

The Phillips cipher splits the text into blocks of size T characters (by default T=5 letters, in which case the blocks are called pentagrams). At the Nth block is associated the grid N (if there are more blocks than grids, the 9th block is again associated with grid 1, and so on).

Example: The message DCODEPHILLIPS is segmented DCODE,PHILL,IPS and DCODE is associated with grid 1, PHILL with grid 2 and IPS with grid 3.

Each letter of a block is then located in the associated grid, and corresponds to a letter encoded according to a shift on the grid of 1 downwards and 1 to the right (offset 1,1). (If this cell does not exist, it is necessary to imagine a continuity of the grid by its opposite side).

Example: D is encrypted by J in the grid \ 1 2 3 4 5 1 A B C D ↴ 2 F G H ↳ J 3 K L M N O 4 P Q R S T 5 U V W X Y and so on, DCODEPHILLIPS is encrypted by JIPJFVDERROVY

\ 1 2 3 4 5 1 A B C D ↴ 2 F G H ↳ J 3 K L M N O 4 P Q R S T 5 U V W X Y

## How to decrypt Phillips cipher?

The Phillips decryption is identical to the encryption, except for the shift in the grid which is reversed. Instead of moving one square to the right and one square down, the decryption performs the reverse path, moving one square to the left and one square to the top.

Example: J is decrypted by D in the grid \ 1 2 3 4 5 1 A B C D ↰ 2 F G H ↖ J 3 K L M N O 4 P Q R S T 5 U V W X Y

\ 1 2 3 4 5 1 A B C D ↰ 2 F G H ↖ J 3 K L M N O 4 P Q R S T 5 U V W X Y

## How to recognize a Phillips ciphertext?

The Phillips cipher can be assimilated to a polyalphabetic cipher, its coincidence index is low between 0.04 and 0.05.

Using a 5x5 grid means that the message consists of up to 25 distinct letters.

Any reference to a screwdriver (Philips is the name given to the cruciform screwdriver) is a clue.

## What are the variants of the Phillips cipher?

Several variants are possible:

— An alternative method of generating the 8 grids, or even not limited to 8 grids.

— The shift of (+1, +1) can very well be modified by any pair (+n, +m)

The block size T may be different, or even vary according to a given split rule.
