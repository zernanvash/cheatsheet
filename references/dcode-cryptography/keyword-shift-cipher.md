# Keyword Shift Cipher

> Source: [https://www.dcode.fr/keyword-shift-cipher](https://www.dcode.fr/keyword-shift-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is a keyword shift cipher? (Definition)

A keyword shift is a classic encryption method that transforms a message by applying a series of alphabetical shifts determined by a keyword.

The shift involves replacing one letter with another slightly further along the alphabet, using a constant value for all letters. A keyword shift relies on several successive shifts.

This method belongs to the family of polyalphabetic ciphers, the most famous historical example of which is the Vigenère cipher .

## How to encrypt using a keyword shift cipher?

The principle of keyword-based ciphers is an improvement in shift ciphering. The shift is to replace one letter with another a little further in the alphabet, it is the method of the figure of Caesar. This technique has only 26 choices of offset and is therefore easily breakable.

The use of a key word makes it possible to define several successive different offsets, deduced from the key word itself, by associating with each letter of the key word an offset. This technique takes the name of polyalphabetic cipher.

Example: ABC can correspond to the shifts 1,2,3 , associating A = 1, B = 2, C = 3, etc, on the principle of Z = 26.

The Vigenere figure is the first use of this kind of encryption, it associates A = 0, B = 1, etc. Z = 25.

## How to decrypt a keyword shift cipher?

Keyword shift decryption involves applying the inverse operation of encryption.

It requires knowing the exact same keyword and the same alphabet (letter-number correspondence) as during encoding.

For each letter of the encrypted message, the shift associated with the corresponding letter of the keyword is subtracted.

If the encryption applied a shift of +N ( modulo 26 ), the decryption applies a shift of -N ( modulo 26 ).

If the encryption shifted the alphabet to the right, the decryption will shift it to the left.
