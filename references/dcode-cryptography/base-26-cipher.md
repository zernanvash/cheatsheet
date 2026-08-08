# Base 26 Cipher

> Source: [https://www.dcode.fr/base-26-cipher](https://www.dcode.fr/base-26-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is Base 26 cipher? (Definition)

Base 26 ( hexavigesimal ) is the arithmetic base using 26 digits/symbols/characters to write numbers. This base can be used with the 26 letters of the alphabet as digits , which makes it possible to numerically encode any word (in both directions: numbers to letters or letters to numbers).

## How to encrypt using Base 26 cipher?

The encoding with base 26 uses an arithmetic base change from base 26 to base 10. The words are considered as written in base 26 (with 26 symbols: the 26 letters of the alphabet ABCDEFGHIJKLMNOPQRSTUVWXYZ ) then converted to base 10 . The resulting decimal number is the encrypted/coded word.

The lookup table is: 0 A 1 B 2 C 3 D 4 E 5 F 6 G 7 H 8 I 9 J 10 K 11 L 12 M 13 N 14 O 15 P 16 Q 17 R 18 S 19 T 20 U 21 V 22 W 23 X 24 Y 25 Z

0 A 1 B 2 C 3 D 4 E 5 F 6 G 7 H 8 I 9 J 10 K 11 L 12 M 13 N 14 O 15 P 16 Q 17 R 18 S 19 T 20 U 21 V 22 W 23 X 24 Y 25 Z

Example: To code DCODE , written in base 26 , convert it to base 10: D=3 , C=2 , O=14 , D=3 , E=4 so $ 3 \times 26^4 + 2 \times 26^3 + 14 \times 26^2 + 3 \times 26^1 + 4 \times 26^0 = 1415626 $

This method is the most rigorous mathematically, but can raise problems for encrypting words starting with A (which corresponds to the 0 symbol in base 10) and is thus generally ignored at the beginning of the number ( 001 = 1 ). It is sometimes considered to use 'A = 1' for some applications in cryptography.

## How to decrypt Base 26 cipher?

Deciphering hexavigesimal ( base26 ) consists of converting base-10 numbers to base-26 (using the 26 letters of the alphabet as symbols). Hexavigesimal numbers then become words.

Example: $ 1415626 = 3 \times 26^4 + 2 \times 26^3 + 14 \times 26^2 + 3 \times 26^1 + 4 \times 26^0 $ so [3,2,14,3,4] in base 26 and 3=D , 2=C , 14=O , 3=D , 4=E . The plain message is DCODE .

By convention, uppercase letters (A-Z) are used but lowercase letters (a-z) are possible.

## How to recognize a Base 26 ciphertext?

The ciphered message is made of numbers, relatively big (for long words)

Identical words are encoded in the same way, so if words (repeated or very common) appear several times in the clear message, the numbers corresponding to them will appear several times in the encoded message.

The calculation of the modulo 26 values of each word makes it possible to find the value of the last letter, which should often be E or S (the most common final letters)

Base 26 allows you to create unique identifiers from a numeric code (customer number, account number, etc.)

## What is the reverse order letters option?

Rather than converting normally, the reverse order of letters can be considered (or the word reversed):

Example: DCODE = $ 3 \times 26^0 + 2 \times 26^1 + 14 \times 26^2 + 3 \times 26^3 + 4 \times 26^4 = 1890151 $ (this is equivalent to coding EDOCD ).

## How to deal with a word starting with 'A'?

as A is encoded 0 in base 26 , when encoding it is null and disappear when decoding.

Example: The code for AB = 0*26^1+1*26^0 = 1 or 1 = B , so it is better to encode 01 .

Alternatively, dCode suggests using 1 as the value for encoding A , thus avoiding the use of the initial 0 .

## How to store words on 32-bit or 64-bit integers?

In computing, integers are usually stored in 32 bits, the largest possible value is $2^{32} - 1 = 4294967295$. Using base 26 , it is therefore possible to store any 6-letter word in an integer (because the largest 6-letter word is ZZZZZZ whose base 10 value is 308915775). With a 64-bit integer, the limit increases to 13 letters.
