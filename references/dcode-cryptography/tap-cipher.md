# Tap Code Cipher

> Source: [https://www.dcode.fr/tap-cipher](https://www.dcode.fr/tap-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is Tap Code? (Definition)

Tap Code , also known as tap cipher, is an encryption method that uses sequences of taps (or sound, or lights) to represent letters in a grid/matrix.

## How to encrypt using Tap code cipher?

The tap code cipher uses a grid of letters, usually 5x5, containing 25 of the 26 letters of the alphabet. The letter that is omitted is often J (replaced by I ) or K (replaced by C ).

The coordinates (row, column) of the cells of the grid are numbered from 1 to 5 and thus any cell has an quivalent pair of digits (row, column)

Example: \ 1 2 3 4 5 1 A B C D E 2 F G H I J 3 L M N O P 4 Q R S T U 5 V W X Y Z

\ 1 2 3 4 5 1 A B C D E 2 F G H I J 3 L M N O P 4 Q R S T U 5 V W X Y Z

Each character of the plain message must be present in the grid otherwise it can not be encoded.

The principle of the tap code is to strike a number of hits corresponding to the coordinates of each character.

Example: D in position 1,4 (row 1 column 4) corresponds to 1 then 4 shots and so DCODE translates to . .... . ... ... .... . .... . .....

## How to decrypt Tap code cipher?

The decryption of the tap code requires knowing the grid and counting the numbers of tap/knock by arranging them in groups of 2 forming the coordinates (row, column) of each letter of the plain message.

Example: To decode the message .... ..... . ... ..... , count the dots (the taps): 4 4 1 1 3 5 , rewrite in groups of 2 (4,4) (1,1) (3,5) and translate these coordinates into letters, respectively T,A,P , so TAP is the message in plain text.

## How to recognize a Tap ciphertext?

The message is composed of a single character repeated between 1 and 5 times, a separator (like / ) can be used, similar to the Morse.

The message can be in the form of a sound or a or light, again repetitive.

The name tap or knock is the onomatopoeia of the noise when the code is tapped or knocked on a surface such as a wall.

On mobile phones, taps can take the form of vibrations.

If tapping can take many forms, then perhaps it is Morse code .

## How to decipher tap cipher without grid?

By default the grid is often the same: composed of the alphabet but without the letter K or the letter J (sometimes the letter Z ), testing these few grids should be enough, otherwise to use a random grid and use the mono-alphabetic substitution decryption tool.

## What are the variants of the knock code cipher?

The grid can have a different size, different content such as a mixed alphabet or even reverse the writing of the coordinates (row-column or column-row).

A 6x6 grid containing 36 characters (26 letters and 10 digits) can be used to encode alphanumeric messages containing words and numbers.

Any communication/tapping containing 6, 7, 8 or more successive taps may indicate something special, a start of a message, an end of a message, a mistake made, etc.

## When was tap code invented?

The code is certainly very old, but there is no specific date. It has been used by prisoners in jails for centuries.

A little more recently, this code was used during the Vietnam War by a certain Captain Carlyle (Smitty) Harris.
