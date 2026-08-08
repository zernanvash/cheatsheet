# Base 36 Cipher

> Source: [https://www.dcode.fr/base-36-cipher](https://www.dcode.fr/base-36-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is Base 36 cipher? (Definition)

Base 36 is a positional numbering system (arithmetic base) using 36 distinct symbols: generally the 36 alphanumeric characters comprising the 26 letters of the alphabet ABCDEFGHIJKLMNOPQRSTUVWXYZ and the 10 digits 0123456789 .

This base allows any word/text consisting of letters and numbers to be converted into a single base-10 number (and conversely, any decimal number corresponds to a sequence of alphanumeric characters in base 36 ).

## How to encode a message via Base 36?

Base-36 encryption is technically a conversion to base-10, using the principle of arithmetic base conversion (converting a text considered to be written in base-36 to base-10).

It is possible to use 2 sets of symbols for base 36 : either digits then letters Alphabet#1 0 1 2 3 … 7 8 9 A B C D … X Y Z Index 0 1 2 3 … 7 8 9 10 11 12 13 … 33 34 35

Alphabet#1 0 1 2 3 … 7 8 9 A B C D … X Y Z Index 0 1 2 3 … 7 8 9 10 11 12 13 … 33 34 35

Or letters then digits Alphabet#2 A B C D … X Y Z 0 1 2 3 … 7 8 9 Index 0 1 2 3 … 23 24 25 26 27 28 29 … 33 34 35

Alphabet#2 A B C D … X Y Z 0 1 2 3 … 7 8 9 Index 0 1 2 3 … 23 24 25 26 27 28 29 … 33 34 35

Example: To code the 3 characters B36 in base 36 using the symbols 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ , first note the base 10 index of each character: B=11 , 3=3 , 6=6 then apply the base change formula: $ 11 \times 36^2 + 3 \times 36^1 + 6 \times 36^0 = 14370 $ the coded message is then 14370 .

## How to decode numbers by writing them in Base 36?

The decryption of decimal numbers (in base 10) to base 36 consists of carrying out the inverse base change of the encryption, namely from base 10 to base 36 .

Example: Decode the message 527198 . $ 527198 = 11 \times 36^3 + 10 \times 36^2 + 28 \times 36^1 + 14 \times 36^0 $ so [11,10,28,14] in base 36 and 11=B , 10=A , 28=S , 14=E . The plain message is BASE .

## How to recognize a Base 36 ciphertext?

The coded message consists of integer numbers whose length is proportional to the length of the word.

The same word is coded with the same number, so the numbers corresponding to the common words appear coded several times.

## Why use Base 36?

Base 36 is useful for several reasons:

— Storage optimization: An alphanumeric string can be converted into a single number ( Base 26 is used to store words).

— Ease of reading, writing, and therefore memorization: a base 36 number is shorter than its base 10 equivalent.

— Use in computer systems for unique identifiers, URL shortening, certain hashing algorithms , etc.

## What are remarkables conversions to Base 36?

Round values in decimal base: Base10 Base36 100 2S 1000 RS 10000 7PS 100000 255S 1000000 LFLS 1000000000 GJDGXS

Base10 Base36 100 2S 1000 RS 10000 7PS 100000 255S 1000000 LFLS 1000000000 GJDGXS

Round values in base36 : Base36 Base10 10 36 100 1296 1000 46656 10000 679616 100000 60466176 1000000 176782336

Base36 Base10 10 36 100 1296 1000 46656 10000 679616 100000 60466176 1000000 176782336
