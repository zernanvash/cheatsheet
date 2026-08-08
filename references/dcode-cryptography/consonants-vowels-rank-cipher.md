# Consonants/Vowels Rank Cipher

> Source: [https://www.dcode.fr/consonants-vowels-rank-cipher](https://www.dcode.fr/consonants-vowels-rank-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## How to encrypt using vowels-consonants rank cipher?

The encryption is based on the position of the vowels (AEIOUY) and consonants (BCDFGHJKLMNPQRSTVWXZ) in the alphabet.

1 B 2 C 3 D 4 F 5 G 6 H 7 J 8 K 9 L 10 M 11 N 12 P 13 Q 14 R 15 S 16 T 17 V 18 W 19 X 20 Z

1 B 2 C 3 D 4 F 5 G 6 H 7 J 8 K 9 L 10 M 11 N 12 P 13 Q 14 R 15 S 16 T 17 V 18 W 19 X 20 Z

1 A 2 E 3 I 4 O 5 U 6 Y

1 A 2 E 3 I 4 O 5 U 6 Y

With these tables, it is then possible to realize various substitutions/encryptions:

Consonants : Each consonant is encrypted by its rank (number indexed from 1 to 20).

Example: DCODE is then encoded: 3,2,O,3,E

Vowels : Each vowel is encrypted by its rank (number indexed from 1 to 6).

Example: DCODE is then encoded: DC4D2

Consonants and Vowels : For this case, it is necessary to distinguish the vowels by the prefix V and the consonants by the prefix C

Example: DCODE is then encoded C3C2V4C3V2

## How to decrypt using vowels-consonants rank cipher?

Deciphering requires replacing the numbers with the corresponding vowels or consonants.

1,2,3 may correspond to 'A, E, I' or 'B, C, D' according to the encryption mode

Example: C3C2V4C3V2 deciphers DCODE

## How to recognize a vowels-consonants rank ciphertext?

The message is composed of numbers, in its most common version, there are many C and V to indicate consonants and vowels respectively.
