# Vigenere Multiplicative Cipher

> Source: [https://www.dcode.fr/multiplication-vigenere-cipher](https://www.dcode.fr/multiplication-vigenere-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## How to encrypt using Multiplication Vigenere cipher?

Vigenere Multiplication Encryption uses a numeric key (some numbers) and a numeric message (use an alphanumeric substitution A1Z26 , or ASCII code for example).

Example: Encode 4,3,15,4,5 (for DCODE ) with the key 11,5,25 (for KEY )

Take the first number of the message and the first number of the key and multiply them, the result is the product 's value. Same for the next numbers of the message and the key.

If the key length is inferior of the text lenght, start over the key.

Example: Calculate 4*11=44 , 3*5=15 , 15*25=375 , 4*11=44 , 5*5=25 to get the cipher message 44,15,375,44,25 Plain numbers 4 3 15 4 5 Key numbers 11 5 25 11 5 Cipher numbers 44 15 375 44 25

Plain numbers 4 3 15 4 5 Key numbers 11 5 25 11 5 Cipher numbers 44 15 375 44 25

## How to decrypt Multiplication Vigenere cipher?

Decryption requires a key and a numeric text.

Example: The ciphered message is 44,15,375,44,25 and the key 11,5,25 (for KEY )

Divide the first number of the message by the second number of the key. Write the result (which must be integer). Same for the next numbers of the message and the key.

Example: 44/11=4 , 15/5=3 etc. The original plain text is 4,3,15,4,5 ( DCODE ).

## How to recognize Vigenere Multiplication ciphertext?

The message is made of numbers with 1 to 5 digits, none is prime.

## How to decipher Vigenere Multiplication without key?

Vigenere multiplication can be cracked by trying to find the length for which GCD of values are the greatest.
