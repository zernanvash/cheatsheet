# Progressive Caesar Cipher

> Source: [https://www.dcode.fr/progressive-caesar-cipher](https://www.dcode.fr/progressive-caesar-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is Progressive Shift? (Definition)

Progressive Caesar's encryption is a variant of the Caesar cipher . Instead of using the position of the letters in the alphabet and shift by X a letter in position N (so taking the letter in position N+X ), the progressive shift consists of taking successively X , X+1 , X+2 etc. as a shift sequence.

## How to encrypt using Progressive Shift cipher?

Progressive shift encryption requires an initial offset value and an increment value.

Example: AAA is encrypted DDD with a Caesar shift of 3 (no incrément)

Example: AAA is encrypted DEF with a progressive Caesar offset of 3 (then 4 , 5 , etc. so increment of 1)

See the shift cipher tool for more options on this type of encryption (shift by letters, by words, etc.).

## How to decrypt using Shift cipher?

The decryption by Caesar Progressive, requires to know the encryption parameters (progressive or decreasing and the mode of shift change).

Decoding consists of shifting the letters of N in the alphabet for the first letter, then N+1 , N+2 and so on, for the following letters.
