# Fractionated Morse Cipher

> Source: [https://www.dcode.fr/fractionated-morse](https://www.dcode.fr/fractionated-morse)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## How to encrypt using fractionated Morse cipher?

The encryption consists, first of all, of encoding the plain message in Morse (point . for short, dash - for long), with a separator | , between each letter, and between each word a double separator || .

Example: DCODE MORSE is encoded in Morse -..|-.-.|---|-..|.||--|---|.-.|...|.||

The morse message is divided into trigrams (groups 3 characters) and completed with . or - if required (for the last one)

Example: -.. , |-. , -.| , ..., ||. (A dot has been added)

Each trigram is then substituted with the following table (read in columns) to get the encoded message.

A B C D E F G H I J K L M N O P Q R S T U V W X Y Z . . . . . . . . . - - - - - - - - - | | | | | | | | . . . - - - | | | . . . - - - | | | . . . - - - | | . - | . - | . - | . - | . - | . - | . - | . - | . -

A B C D E F G H I J K L M N O P Q R S T U V W X Y Z . . . . . . . . . - - - - - - - - - | | | | | | | | . . . - - - | | | . . . - - - | | | . . . - - - | | . - | . - | . - | . - | . - | . - | . - | . - | . -

Example: -.. corresponds to J , |-. for V , -. for L , etc. The final encrypted message is JVLNVGZQODSGY

It is possible to mix the order of the letters of the alphabet to complicate the decryption.

## How to decrypt fractionated Morse cipher?

The fractionated Morse decryption requires to know the table used for the encryption (possibly generated with a disordered alphabet or a key).

Each letter of the encrypted message is re-associated with the corresponding trigram .

Example: The message ONTGCI gives --|---|.-.|...|.||

The plain message is then obtained by deciphering this code in Morse (with | as the letter separator).

Example: The decoded plain message is MORSE .

Sometimes a final letter is erroneous or appears in addition to the original message, this is due to the completion in trigrams during the encryption process.

## How to recognize a fractionated Morse ciphertext?

The message is composed of letters and has a coincidence index a little lower than that of the language of the plain text.

Some bigrams or trigrams can never appear as IS , IT , ... IZ or RS , RT , ... RZ because they would introduce three separators ||| which is impossible.

Frequency analysis of trigrams and quadrigrams can give a good estimate of the position of the words THE , OF , etc. in the text.

## What are the variants of the fractionated Morse cipher?

During encryption, the first row of the table is the alphabet used, a deranged alphabet , or an alphabet generated from a key is also a possibility.
