# Letter Number Code (A1Z26) A=1, B=2, C=3

> Source: [https://www.dcode.fr/letter-number-cipher](https://www.dcode.fr/letter-number-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is the A1Z26 cipher? (Definition)

The Letter-to-Number Cipher (or Number-to-Letter Cipher or numbered alphabet ) consists in replacing each letter by its position in the alphabet , for example A=1, B=2, Z=26, hence its over name A1Z26 .

## How to encrypt using Letter-to-Number/A1Z26 cipher?

A1Z26 encryption requires to count the positions/ranks of letters in the alphabet. If it is the Latin alphabet of 26 characters here is the correspondence table letter ↔ number/value:

A B C D E F G H I J K L M N O P Q R S T U V W X Y Z 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26

A B C D E F G H I J K L M N O P Q R S T U V W X Y Z 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26

Replace each letter with its position in the alphabet (A = 1, B = 2, … Z = 26) and use a separator character to space the numbers.

Example: DCODE is encrypted 4-3-15-4-5 by alphanumeric substitution

Often the space character is translated with the number 0

## How to decrypt Number-to-Letter cipher?

Decryption requires taking each number and replace it with the letter of same position in the alphabet : 1 = A, 2 = B, … 26 = Z, here is the corresponding table:

1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 A B C D E F G H I J K L M N O P Q R S T U V W X Y Z

1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 A B C D E F G H I J K L M N O P Q R S T U V W X Y Z

Example: 1.12.16.8.1.2.5.20 gives ALPHABET

The A1Z26 cipher is a very simple and easily decipherable cipher. It is mainly used for educational or recreational purposes.

## How to recognize Letter-to-Number ciphertext?

The crypted message is made of numbers between 1 and 26, sometimes the number 0 is used to code a space.

Numbers are usually separated by spaces or dashes.

The digit 5 for E is supposed to appear regularly for an English text.

This encryption is sometimes called alphanumeric code .

If the alphabet is shifted, it is common for clues of the form letter equals number (K=7) to be provided (common principle of cryptogram type games).

## What are the variants of the Letter-to-Number cipher?

Shift of numbers: the alphabet can start with A = 0 (A0Z25) or A = 1, but also A = 65 or A = 97 ( ASCII code ).

Use of a supplementary character for space (often 0, more rarely 27)

Use of leading zeros to be able to concatenate numbers AB = 0102 , else AB = 12 and 12 = L .

Using a distorted, shifted alphabet ( Caesar cipher ), or even an inversion of the alphabet (A=26, Z=1), or random values for each letter

Use of modulo 26 in order to get 1=A,2=B,…26=Z then 27=A, 28=B etc.

## How to program the A1Z26 code?

The A1Z26 encoding/decoding algorithm is as follows: // Pseudo code function encrypt_A1Z26(text) { dictionary = {"A":1, "B":2, . . ., "Z":26} ciphertext = "" foreach (letter in text) { ciphertext += dictionary.replace(letter) + "-" } return ciphertext } function decrypt_A1Z26(text) { dictionary = {1:"A", 2:"B", . . ., 26:"Z"} text.split("-") plaintext = "" foreach (number in text) { plaintext += dictionary.replace(number) } return plaintext } // Python def encode_a1z26(text): return " ".join(str(ord(c) - 64) for c in text.upper() if c.isalpha()) def decode_a1z26(numbers): return "".join(chr(int(n) + 64) for n in numbers.split())
