# Atbash Cipher

> Source: [https://www.dcode.fr/atbash-cipher](https://www.dcode.fr/atbash-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is Atbash cipher? (Definition)

The Atbash cipher (also called the mirror cipher or reverse alphabet ) is a monoalphabetic substitution cipher in which each letter is replaced by its counterpart in the alphabet; thus, A becomes Z , B becomes Y , and so on.

This cipher takes its name and origins from the ancient Hebrew alphabet.

## How to encrypt using Atbash cipher?

The Atbash cipher relies on an inverted alphabet that serves as a reversible substitution key.

The Latin alphabet ABCDEFGHIJKLMNOPQRSTUVWXYZ and its symmetrical inverse (mirror) ZYXWVUTSRQPONMLKJIHGFEDCBA are mapped in a substitution table:

Normal ABCDEFGHIJKLMNOPQRSTUVWXYZ Reverse ZYXWVUTSRQPONMLKJIHGFEDCBA

Normal ABCDEFGHIJKLMNOPQRSTUVWXYZ Reverse ZYXWVUTSRQPONMLKJIHGFEDCBA

Encryption consists in replacing letters from the first with letters from the other one, with is equivalent to replace the first letter of the alphabet A with the last one Z , the second one B with the penultimate Y etc.

Example: MIRROR becomes NRIILI

## How to decrypt Atbash cipher?

Atbash decryption is identical to encryption, since the substitution (mirror) alphabet is reversible (due to the symmetry of the backwards alphabet ).

Example: ZGYZHS is decrypted ATBASH

dCode offers an encoder and a decoder, but they are actually one and the same Atbash tool/converter.

## How to recognize an Atbash ciphertext?

An Atbash ciphertext has a coincidence index similar to an unencrypted text.

If the encryption used the classical latin alphabet, letters V,G,R,L,M appear the most frequently.

Otherwise the presence of Hebrew characters or a reference to the Dead Sea can be a clue.

The notions of mirror, reflection, opposite, axis, direction, word written in reverse (hsabta) are also clues.

## Why is this cipher called 'Atbash'?

The name Atbash comes from the method applied to the Hebrew alphabet:

— A leph (first letter) ↔ T av (last)

— B eth (second) ↔ Sh in (penultimate)

The initials of these four letters ( A-T-B-Sh ) form the word Atbash .

## How is the Atbash number used in the Hebrew Bible?

The number Atbash is mentioned in the Hebrew Bible , notably in the book of Jeremiah (chapter 25, verse 26 and chapter 51, verse 41). It is used to replace names and places with their coded equivalents.

Example: The word ששך Sheshakh is the Atbash equivalent of בבל Bavel (Babylon)

## What dictionary words still exist when encrypted?

There are a small number of words that have an existing Atbash equivalent in the English dictionary.

Example: GIRTH & TRIGS , GIRL & TRIO , GLOW & TOLD , HOLD & SLOW , HORN & SLIM , WILD & DROW , ZARA & AZIZ

In Hebrew, this situation is more common (notably because the alphabet has no vowels).

## What are Atbash variants?

Atbash can be applied to any alphabet (Latin, Greek, Hebrew, Cyrillic, etc.)

Mathematically, it is a special case of the affine cipher where the multiplicative parameter is $ a = n-1 $ and the offset $ b = n-1 $ with $ n $ the size of the alphabet.

Atbash can be described as a monoalphabetic substitution using the reversed alphabet ZYXWVUTSRQPONMLKJIHGFEDCBA

## When was Atbash invented?

The origins of the Atbash cipher date back to antiquity, probably around the 6th or 5th century BC, in Israel.

It is considered one of the earliest known cipher systems, used primarily for symbolic or religious purposes rather than for security.
