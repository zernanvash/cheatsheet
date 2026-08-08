# Homophonic Cipher

> Source: [https://www.dcode.fr/homophonic-cipher](https://www.dcode.fr/homophonic-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is the Homophonic cipher? (Definition)

The homophonic cipher is a substitution cipher that uses a correspondence table between the letters / characters of the plain message and one or more letters / numbers / groups of characters.

Consequently, the same letter may have several possible encryption and the same message will possibly have several possible encrypted versions.

The homophonic cipher helps hide the frequency of letters used in a message, thus making frequency analysis more difficult for a cryptanalyst.

## How to encrypt using Homophonic cipher?

To use the homophonic cipher , the user must first define a correspondence table between the plain text characters and one or more symbols for each character.

During the encryption process, randomly choose from these symbols each time a specific character needs to be encoded. This ensures that the same character is not always represented by the same symbol in the ciphertext.

Example: Using the nomenclature A(45,96,17) , B(37,60) , C(05,88) , it is possible to code ABC as 45,60,88 or 96,60,05 or 96,37,05 etc.

To maximize encryption security, it is smart to use a number of matches per letter proportional to the frequency of the letter in the language of the clear message, and be sure to select a replacement from the list randomly.

## How to decrypt an Homophonic cipher?

Use the correspondence table to transform each character / group of characters in the plain message.

Example: 34,25,10 has been coded with these multiple correspondences: A(87,34,11) , B(25,80) , C(10,55) , the plain message is ABC

## How many correspondences to use per letters?

By taking 100 numbers, the ideal match is approximately equal to the frequency of each letter in the English language (expressed as a percentage rounded to the nearest unit)

E 12 T 9 A 8 O 7 I 7 N 7 S 6 H 6 R 6 L 4 D 4 C 2 U 2 M 2 W 2 F 2 G 2 Y 2 P 2 B 2 V 1 K 1 J 1 X 1 Q 1 Z 1

E 12 T 9 A 8 O 7 I 7 N 7 S 6 H 6 R 6 L 4 D 4 C 2 U 2 M 2 W 2 F 2 G 2 Y 2 P 2 B 2 V 1 K 1 J 1 X 1 Q 1 Z 1

Using 50 numbers, roughly divide the quantities by 2.

Using the pieces of a Scrabble game is a good idea.

## How to recognize an homophonic ciphertext?

When well done, the frequency of characters in a homophonically encrypted message is close to that of a perfectly random text, its index of coincidence too.

In order to simplify the work of the receiver of the message, it is common to use groups of numbers/letters of fixed length (2 or 3 digits).

If the correspondence table is accessible, the figure becomes a classic substitution system.

## Why use a homophonic number?

Using a homophonic cipher makes the ciphertext more resistant to frequency analysis methods.

In cryptography, hiding the frequency of letters in text helps protect against decryption attempts that exploit this information.

## How to decipher homophonic without correspondence table?

If the correspondences are proportional to the frequency of characters in the language of the plain message, then it is impossible to use frequency analysis or coincidence index techniques.

From a portion of known or assumed text, it is possible to guess a few correspondences of some characters but it is often insufficient to decipher the whole message.
