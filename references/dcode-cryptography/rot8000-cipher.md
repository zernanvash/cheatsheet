# ROT8000 Cipher

> Source: [https://www.dcode.fr/rot8000-cipher](https://www.dcode.fr/rot8000-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is ROT8000 cipher? (Definition)

ROT8000 is short for rotation 0x8000, which is a mono-alphabetic substitution method that replaces each character with another approximately 32768 positions later in the Unicode repository.

In reality, the encoding is limited to the basic multilingual plane (BMP) of the Unicode encoding which consists of the first 65536 characters, and moreover, certain (control) characters are ignored. The rotation is therefore not exactly 0x8000.

## How to encrypt using ROT8000 cipher?

The ROT8000 code consists of replacing each character by shifting on the Basic Multilingual Plane from which the control characters have been removed (there are then 63404 characters left).

Example: The character A of Unicode point code U+0065, is then coded 籊 U+7C4A (shift of 31753)

## How to decrypt ROT8000 cipher?

Since the rotation is calculated to cover half of the Basic Multilingual Plane (BMP) (32768 out of 65536 characters), decryption is identical to encryption.

In other words, encrypting a text twice by ROT8000 makes it possible to find the original message.

## How to recognize a ROT8000 ciphertext? (Identification)

Unicode characters associated with basic Latin characters (a-z A-Z 0-9, etc.) are encoded by sinograms (Chinese characters)

Example: 籪籫籬籭籮籯籰籱籲米籴籵籶籷籸籹籺类籼籽籾籿粀粁粂粃 籊籋籌籍籎籏籐籑籒籓籔籕籖籗籘籙籚籛籜籝籞籟籠籡籢籣 簹簺簻簼簽簾簿籀籁籂

## What are ignored caracters?

The space character (U+0020) is ignored (just like the other space variants) as well as the control characters from U+0000 to U+001F, from U+007F to U+00A0 and from U+D800 to U +DFFF.

## Why emojis are not converted?

ROT8000 support is limited to BMP, and emojis are not included in this Unicode plan (just like thousands of other characters).
