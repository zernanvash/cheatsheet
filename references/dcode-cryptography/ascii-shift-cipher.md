# ASCII Shift Cipher

> Source: [https://www.dcode.fr/ascii-shift-cipher](https://www.dcode.fr/ascii-shift-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is ASCII Shift cipher? (Definition)

The ASCII shift cipher is a substitution cipher method, which, as its name suggests, will use the ASCII table and shift each character by a certain number of positions.

This process is an extension of the Caesar cipher (which is limited to letters) to all ASCII characters (i.e. alphabetic, uppercase, lowercase , numeric and symbolic).

## How to encrypt using ASCII Shift cipher?

To encode a text with the ASCII shift cipher:

— Identify the ASCII code of each character in the plain text (the ASCII table is composed of 128 characters with a code between 0 and 127).

— Add a fixed numerical shift (also called the encryption key) to each ASCII code . This key can take the format of a number (between 1 and 127, negative numbers are possible, this amounts to a shift in the other direction) or an ASCII character (in this case the character code is used as a number).

— Convert the new codes into characters to obtain the encrypted text. The shift is circular (moving after the end of the alphabet returns to the beginning), if the code is greater than or equal to 128, the limit of the ASCII table , return to the beginning 0.

Example: A ( ASCII code 65 ) shifted by 40 becomes the code 105 (65 + 40 = 105) or i ( ASCII code 105 ).

The ASCII code includes non-printable characters, which dCode displays with � , use decimal or hexadecimal formats to not lose information on display.

## How to decrypt ASCII Shift cipher?

Decrypting an ASCII offset is the same as encrypting it, but with the offset in the other direction. Instead of adding, the operation is to subtract the offset used during encryption (the equivalent of encrypting with a negative offset).

Example: The encrypted message SeU[[qUaVW shifted from -18 decodes ' ASCII_CODE '

## How to recognize a ASCII Shift ciphertext?

The message is composed only of ASCII characters.

Frequency analysis should emphasize groups of characters more often (those corresponding to the letters of the plain message).

## How to decipher ASCII Shift without knowing the shift?

dCode allows you to test the 127 offsets and displays the most probable results automatically.

## What are the variants of the ASCII Shift cipher?

The shift ciphers are numerous, the most known is the Caesar cipher , but ROT-47 is probably the closest to ASCII shift as it is limited to printable characters and is reversible.
