# Prime Numbers Cipher

> Source: [https://www.dcode.fr/prime-numbers-cipher](https://www.dcode.fr/prime-numbers-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is a prime numbers subsitution cipher? (Definition)

Substitution by prime numbers, as the name suggests, is a cipher in which letters are replaced by prime numbers. By default, replace the 26 letters of the alphabet with the 26 first prime numbers ( A=2 , B=3 , C=5 , D=7 , …, Z=101 ).

## How to encrypt using Prime Numbers cipher?

The encryption uses a correspondence between prime numbers and letters. A 2 B 3 C 5 D 7 E 11 F 13 G 17 H 19 I 23 J 29 K 31 L 37 M 41 N 43 O 47 P 53 Q 59 R 61 S 67 T 71 U 73 V 79 W 83 X 89 Y 97 Z 101

A 2 B 3 C 5 D 7 E 11 F 13 G 17 H 19 I 23 J 29 K 31 L 37 M 41 N 43 O 47 P 53 Q 59 R 61 S 67 T 71 U 73 V 79 W 83 X 89 Y 97 Z 101

Example: DCODE is crypted 7,5,47,7,11

## How to decrypt Prime Numbers cipher?

Decryption requires knowing the correspondence used between prime numbers and letters. By default, A=2 , B=3 , C=5 , …

Example: The cipher message 53,61,23,41,11 will be decrypted into PRIME

## How to recognize a Prime Numbers ciphertext?

The message is only made of prime numbers, mainly the first 26 prime numbers: $ 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101 $

## What are the variants of the Prime Numbers cipher?

It is possible to define an alternative correspondence (or random) between prime numbers and letters.

Example: Random substitution: A=17 , B=43 , C=101 , D=3 , etc.

To decode this alternative, convert the numbers into letters using the decryption form and then perform a monoalphabetic substitution .

The prime multiplication cipher (rarely called South African Scouts Cipher) uses prime numbers that are multiplied together. A prime decomposition is necessary.

Example: 110 = 2*5*11 = A,C,E .

In this case, the order of letters is not necessarily preserved ( ACE=2*5*11=110 and ECA=11*5*2=110 too), an anagram generator or a permutations generator is useful to find back the right permutation of letters.
