# Ideograms Cipher (Lines, Circles, Dots)

> Source: [https://www.dcode.fr/ideograms](https://www.dcode.fr/ideograms)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## How to encrypt using Ideograms?

Ideograms encryption associates to each letter of the plain text, a number, which is decomposed in (any) distinct values

Example: The message be encrypted is DCODEZ , initially coded by ( alphabetic rank ) 4, 3, 15, 4, 5, 26 and selected values are 10 , 5 and 1 for decomposition. D = 4 = 0*10 + 0*5+ 4*1 O = 15 = 1*10 + 1*5 + 0*1 Z = 26 = 2*10 + 1*5 + 1*1

Each values corresponds to a selected form (basic element such as a point, a line, a line, a circle, etc.).

Example: A line = 10, a circle = 5, a dot = 1.

Draw any ideogram with these items.

Example: Z can be drawn ||o. or |.o_

## How to decrypt some Ideograms?

Ideaograms decryption requires decomposing each ideogram in basic forms (generally between 2 and 4 distinct, the most used are dot, circle, line)

Example: Decrypt the message :: .: ∅ .... o

Count the number of appearance of each basic form in each ideogram . :: and .... = 4 dots .: = 3 dots ∅ = 1 circle et 1 line o = 1 circle

Then search for values for each basic element. The value of an ideogram is given by addition .

Example: Values are line = 10, circle = 5, dot = 1. Then :: =4 .: =3 ∅ =15 .... =4 o =5

Each value corresponds to a letter, for example, the alphabetic rank (A=1, B=2, etc.)

Example: The original plain text is DCODE .

## How to recognize Ideograms ciphertext?

The ciphered message is composed of symbols nearly all distinct, with common factors (geometry, color, size, etc.)

## How to decipher Ideograms without values?

One can crack Ideograms with difficulties by testing all values. Note that the value 1 appears often.

## What are the variants of the Ideograms ciphering?

Use of colors (or any distinctive element) rather than geometric forms.

Modification of the addition calculus (eg. a color means a multiplication by N, etc.)
