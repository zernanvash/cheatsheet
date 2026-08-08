# Autoclave Cipher

> Source: [https://www.dcode.fr/autoclave-cipher](https://www.dcode.fr/autoclave-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is an Autoclave cipher? (Definition)

Autoclave/Autokey encryption is a variant of key encryption, it has the particularity of modifying the key by concatenating the key and the message (key+message).

## How to encrypt using Autoclave cipher?

Autoclave encryption uses a cryptographic algorithm with a key (all algorithms are not compatible).

Example: If the key is SECRET . To encode AUTOCLAVE with Autoclave , code normally with the chosen algorithm but with the key SECRETAUTOCLAVE .

Apply the selected algorithm to the plain text: the key self changes the encrypted message.

Example: The key is no longer SECRET but SECRETAUTOCLAVE , the message encrypted by Vigenere is no longer SYVFGESZG but SYVFGEAPX .

The size of the initial key must be smaller than the text size for the autoclave to work.

## How to decrypt Autoclave cipher?

Autoclave decryption requires knowing the chosen algorithm and the initial key.

Example: Decrypt the ciphered message SYVFGEAPX (crypted with Vigenere Autokey ) and the key KEY .

The decryption begins normally for known letters of the key.

Example: Decryption of SYVFGE with the key SECRET gives AUTOCL (the first letters of the plain text).

Next deciphering steps uses as key the first plain letters.

Example: Decryption of the next letters APX with the first letters of the plain text AUT as key gives AVE . The plain text is AUTOCLAVE .

## How to recognize an Autoclave ciphertext?

Using Autokey changes properties of the ciphertext, generally the index of coincidence is lower than a normal index for a given algorithm.

## How to decipher Autoclave without the key?

No magic method, but testing all one-letter keys can be useful. Indeed, key length can be short, it will be completed with plain text.

dCode offers a bruteforce mode that tries to find the probable length of the key, by testing different lengths of keyword. For each letter, dCode attempts to maximize the probability that the text will be plain by frequency analysis . (Method suggested by LeSingeMalicieux)

## What is an Autoclave?

Autoclave is the name of an industrial device that makes it possible to expose elements to high pressures and temperatures.

Autoclave is the name of a rock band and the name of an album of that same band.
