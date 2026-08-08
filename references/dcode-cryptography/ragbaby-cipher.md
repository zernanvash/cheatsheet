# Ragbaby Cipher

> Source: [https://www.dcode.fr/ragbaby-cipher](https://www.dcode.fr/ragbaby-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is Ragbaby? (Definition)

Ragbaby is a polyalphabetic substitution cipher using a progressive shift.

## How to encrypt using Ragbaby cipher?

Encryption with Ragbaby uses the word division of a text as well as a disordered alphabet .

For each word, numbered i (ranging from 1 to N), each letter, numbered j (ranging from 0 to M) is shifted by i+j in the alphabet.

Example: Encrypt the 2 words RAG BABY with the alphabet ALPHBETCDFGIKMNOQRSUVWYZ , to obtain SPM THDH Plain letter R A G B A B Y word i 1 1 1 2 2 2 2 letter j 0 1 2 0 1 2 3 i+j 1 2 3 2 3 4 5 Cipher letter S P M T H D H

Plain letter R A G B A B Y word i 1 1 1 2 2 2 2 letter j 0 1 2 0 1 2 3 i+j 1 2 3 2 3 4 5 Cipher letter S P M T H D H

It is important to define words and their divisions , such as whether a hyphenated word counts as 1 or 2 words.

## How to generate the keyed alphabet?

The alphabet is generated from a keyword, whose repeated letters are removed before adding the rest of the letters of the alphabet in order.

Example: SECRET generates SECRTABDFGHIJKLMNOPQUVWXYZ

In the original version, the author describes an alphabet of only 24 letters, by removing the J (replaced by I ) and the X (replaced by W ).

## How to decrypt Ragbaby cipher?

Ragbaby is an encryption by shift , it is then necessary to calculate the shifts (i+j) for each letter and to subtract this value in the alphabet for each letter of the encrypted message (inverse operation of the encryption).

## How to recognize a Ragbaby ciphertext? (Identification)

Ragbaby necessarily has spaces (or other limiter) to separate the words.

In the original version, only 24 letters are used (no J or X ).

## What are the variants of the Ragbaby cipher?

The alphabet and its size are configurable.

The first word is shifted by 1 , it is possible to take another value.

Each letter induces an additional shift of 1 , it is possible to shift more.

## When was Ragbaby invented?

Ragbaby was proposed by Sherlac, a member of the ACA (American Cryptogram Association) in 1955.
