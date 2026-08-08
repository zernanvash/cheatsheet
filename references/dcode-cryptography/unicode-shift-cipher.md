# Unicode Shift

> Source: [https://www.dcode.fr/unicode-shift-cipher](https://www.dcode.fr/unicode-shift-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is Unicode shifting? (Definition)

Each character has a unique identifier (a number called a code point) in the Unicode repository. By adding a value N to this number, then a different character is identified which can make it possible to create a substitution cipher by character shift, like the Caesar code .

## How to encrypt using Unicode shifting cipher?

For each character in the plain message, note its numeric value (its code point) and add a shift/an offset value N.

Example: The Unicode symbol 🔑 (U+1F511) has the code point 128273 , adding +23 to it the code point 128296 which is the symbol 🔨 (U+1F528)

## How to decrypt Unicode shifting cipher?

For each character of the encrypted message, note its numerical value (its code point) and subtract the offset value N.

Example: Decrypt the coded message ԶԕՁԶԷ with offset 1234 . The corresponding Unicode code points are 1334,1301,1345,1334,1335 subtracting 1234 from it, the plain values are 100,67,111,100,101 i.e. the dCode characters

## How to recognize a Unicode shifted ciphertext? (Identification)

A clear message composed of the usual alphanumeric characters (from the ASCII code ) tends to have codes between 32 and 127, i.e. a spread over a few dozen values.

If such a message is shift-encrypted, then the post-shift dot codes will not be spread any further, the spread should remain within the same range.

If the offset is significant (number greater than 100 or 1000 then the message will only be composed of exotic characters, from non-Latin alphabets or symbols/emoji)

## How to decipher Unicode shift without shift value? (Attacks)

Analyze the values of the smallest code point and of the largest code point, to deduce an average value of the shift.

The Unicode shift cipher (but also in general) remains a substitution and is therefore attackable by frequency analysis : the most frequently encoded characters are the most frequently used characters in the plain message (usually the letter E ).

Upper and lower case are distinct with a Unicode shift cipher.

## What are the variants of the Unicode shift cipher?

ROT8000 is a variant of ROT-13 or ROT-47 adapted to Unicode with a rotation of 0x8000 ( hexadecimal value) but with some adjustments.
