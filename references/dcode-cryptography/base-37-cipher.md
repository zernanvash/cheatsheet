# Base 37 Cipher

> Source: [https://www.dcode.fr/base-37-cipher](https://www.dcode.fr/base-37-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is Base 37 cipher? (Definition)

Base 37 is an arithmetic base made up of 37 symbols. It is used in practice to store text with the 36 alphanumeric characters (26 letters of the alphabet ABCDEFGHIJKLMNOPQRSTUVWXYZ and 10 digits 0123456789 ) accompanied by an additional character, a separator such as space or underscore _ (low dash).

Any whole number (in base 10, decimal) has a base 37 conversion (therefore a writing with the 37 characters above), and conversely any word or sentence (using these 37 symbols) has a base 10 conversion .

## How to encrypt using Base 37 cipher

Base 37 encryption is based on arithmetic base change calculations (the conversion from base 37 to base 10).

Example: To code the 3 characters B37 in base 37 using the 37 symbols 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_ , start by converting each character to base 10 according to their value/rank: B=11 , 3=3 , '7= 7' and apply the base change: $ 11 \times 37^2 + 3 \times 37^1 + 7 \times 37^0 = 15177 $

Several sets of 37 symbols are possible for the base 37 , they differ according to the order of the elements (digits, letters, separator).

Mathematically, the most used is 09AZ_ (numbers, letters, separator) Symbols 0 1 2 3 … 8 9 A B C … X Y Z _ Values 0 1 2 3 … 8 9 10 11 12 … 33 34 35 36

Symbols 0 1 2 3 … 8 9 A B C … X Y Z _ Values 0 1 2 3 … 8 9 10 11 12 … 33 34 35 36

In cryptography, it is preferred AZ09_ (letters, numbers, separator) Symbols A B C … Y Z 0 1 2 3 … 7 8 9 _ Values 0 1 2 … 24 25 26 27 28 29 … 33 34 35 36

Symbols A B C … Y Z 0 1 2 3 … 7 8 9 _ Values 0 1 2 … 24 25 26 27 28 29 … 33 34 35 36

But it is possible to use other combinations , such as those starting with the separator _AZ09 or _09AZ , or the variant 09_AZ or AZ_09 .

## How to decrypt Base 37 cipher

Base-37 decryption is the conversion of encoded numbers (in base 10) to the base 37 .

Example: Decode the message 571923 . $ 571923 = 11 \times 37^3 + 10 \times 37^2 + 28 \times 37^1 + 14 \times 37^0 $ so [11,10,28,14] in base 37 and 11=B , 10=A , 28=S , 14=E , that gives the plain message BASE .

## How to recognize a Base 37 ciphertext?

A base 37 code is theoretically made up of a single large decimal number of length proportional to that of the message.
