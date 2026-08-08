# Nihilist Cipher

> Source: [https://www.dcode.fr/nihilist-cipher](https://www.dcode.fr/nihilist-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is the Nihilist cipher? (Definition)

The nihilist cipher is a super-cipher of the Polybius square . The Polybius square is a substitution cipher where each letter is replaced by a pair of numerical coordinates (row, column) in a grid. The nihilist cipher adds a repeated numerical key to these coordinates, according to a term-by-term addition .

## How to encrypt using Nihilist cipher?

The nihilist 's cipher uses a grid (usually 5x5 = 25 cells) that is filled with letters of the alphabet (often a deranged alphabet ). For a 5x5 grid and the 26-letter latin alphabet, choose a letter to omit, often the J , V or W are omitted. The grid has digit headers for its rows and columns (typically 1 to 5).

Example: \ 1 2 3 4 5 1 A B C D E 2 F G H I J 3 K L M N O 4 P Q R S T 5 U V X Y Z

\ 1 2 3 4 5 1 A B C D E 2 F G H I J 3 K L M N O 4 P Q R S T 5 U V X Y Z

To encrypt a text, it is necessary to replace each letter of the initial text, by its coordinates in the grid. Generally, the coordinates [row, column] (and more rarely [column, row]) are used. A numerical code consisting of pairs of digits is obtained.

Example: A is therefore coded 11 (because in row 1 , column 1 ), E becomes 15 (row 1 , column 5 ).

Example: The message to be encrypted: KREMLIN , which is therefore encoded 31,43,15,33,32,24,34

The particularity of the Nihilist cipher in relation to the Polybius cipher is its over-encryption. The nihilists use a key that is added for each couple of digits previously created.

The result of the addition is theoretically between 22 and 110. There are 2 ways of writing the result, either by separating the numbers (a space or a comma), or by concatenating them, in this way, for the 3-digits numbers keep only the last 2 digits (subtract 100 from sums that would be greater than 100).

Example: The key VODKA , which is coded 52,35,14,31,11 , is added (value after value) to the encrypted text.

Example: Plain Message K R E M L I N Coded (Message) Letters 31 43 15 33 32 24 34 Key (repeated) V O D K A V O Coded (Key) Letters 52 35 14 31 11 52 35 Final Message ( Addition ) 83 78 29 64 43 76 69

Plain Message K R E M L I N Coded (Message) Letters 31 43 15 33 32 24 34 Key (repeated) V O D K A V O Coded (Key) Letters 52 35 14 31 11 52 35 Final Message ( Addition ) 83 78 29 64 43 76 69

Example: The final encrypted message is 83782964437669

## How to decrypt a Nihilist ciphertext?

Decryption requires to know the grid and the over-encryption key.

The message can have the form of a list of numbers (2 or 3 digits) or of a large series of digits, in the second case, separate them into pairs of 2 digits.

Example: The encrypted message 577066392880 , the key CODE and the grid \ 1 2 3 4 5 1 A B C D E 2 F G H I J 3 K L M N O 4 P Q R S T 5 U V X Y Z

\ 1 2 3 4 5 1 A B C D E 2 F G H I J 3 K L M N O 4 P Q R S T 5 U V X Y Z

To decrypt, the coded key is subtracted from each pair of 2 digits and each number obtained is replaced by the corresponding letter with these coordinates in the grid.

Example: The key CODE is coded with the grid 13,35,14,15 , it is then subtracted from the message: Coded Message 57 70 66 39 28 80 Coded Key (repeated) 13 35 14 15 13 35 Subtraction 44 35 52 24 15 45 Letter in the Grid S O V I E T

Coded Message 57 70 66 39 28 80 Coded Key (repeated) 13 35 14 15 13 35 Subtraction 44 35 52 24 15 45 Letter in the Grid S O V I E T

Example: The plain message is SOVIET .

## How to recognize a Nihilist ciphertext?

In the general case of using a 5x5 grid with coordinates from 1 to 5, the message is composed of numbers with the following properties:

— If the encryption is without a separator, the numbers are between 00 and 99 and the message is composed of an even number of digits.

— If the encryption is with separating spaces, the numbers are between 22 and 110

— In all cases, the numbers 11,12,13,14,15,16,17,18,19,20,21,31,41,51,61,71,81,91 can never appear by addition because they contain only one ten or only one unit.

Any reference to Russia (USSR), tsars or Russians traditions is a clue.

The presence of historical figures like Sergei Nechaev or other key figures of Russian nihilism is a significant indicator.

The word nihilist is generally associated with a philisophic doctrine, but in Russian the word нигилизм has a Latin root meaning nothing .

## How to decipher a nihilist text without key?

Without the key, the user must exploit the repeated additive structure. Each block is the sum of two numbers between 11 and 55. It is possible to test hypotheses about key length and then examine the differences between blocks spaced a multiple of that length apart.

dCode analyzes the pairs of digits in the message to extract the potential sums they formed. It is then possible to find all possible combinations and deduce the potential keys using the grid.

## How to decipher a nihilist text without grid?

If the key is known but not the grid, subtraction allows us to recover numerical coordinates.

These coordinates correspond to an unknown grid: the resulting message is then equivalent to a Polybius square , that is, a text encrypted by a monoalphabetic substitution depending on the internal permutation of the grid.

A standard frequency analysis then allows us to progressively reconstruct the grid; see the page dedicated to the Polybius cipher .

## What are the variants of the nihilist cipher?

It is possible to make several variants:

— Inversion of coordinates : rather than using [row, column], it is possible to use [column,row].

— Change of coordinates names : the digits from 1 to 5 can very well be mixed or replaced by other digits.

— Multiple keys , it is possible to use several keys, summed successively, but this only extends the process time and does not complicate a brute-force attack.

## When the Nihilists cipher was invented?

The number of nihilists is associated with 19th-century Russian revolutionary movements, particularly during the period 1860-1880.
