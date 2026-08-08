# Variant Beaufort Cipher

> Source: [https://www.dcode.fr/variant-beaufort-cipher](https://www.dcode.fr/variant-beaufort-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is the Beaufort Variant Cipher? (Definition)

The Variant Beaufort cipher, also called the German Beaufort cipher, is a variant of the classical Beaufort cipher (itself a Vigenère variant). The German version removes the key from the plaintext. This change makes the cipher non-symmetrical, unlike the classical Beaufort cipher.

## How to encrypt using Variant Beaufort cipher?

Encryption is a variant of the Beaufort cipher, so it uses a key (and an alphabet). More precisely, Beaufort encryption is equivalent to Vigenere decryption.

Example: Encrypt the plaintext DCODE with KEY as keyword and the latin alphabet ABCDEFGHIJKLMNOPQRSTUVWXYZ

Each letter has the value of its rank in the latin alphabet from 0=A,1=B,…,25=Z

Example: DCODE is first coded to 3,2,14,3,4 and KEY to 10,4,24

Encryption consists in subtracting the key to the plain text. Calculation is made letter after letter (ie. their rank/value in the alphabet ). In case of negative result, add 26 to the result (with 26 the length of the alphabet). The key is repeated (if needed) until it fits the plain text's length: KEYKEYKEYK…

Example: Subtract the first letter of the key K (=10) to the first letter of the plain message D (=3) : 3-10=-7. As the result is negative, add 26. -7+26= 19 . Save this result and go on with next letters: the 2nd letter of the plain message C and the 2nd letter ot the key E : 2-4=-2+26= 24 . Keep going with the third letters O and Y : 14-24=-10+26= 16 . At the 4th step, arrived at the end of the key, repeat the key (or go to the beginning, its the same), subtract the first letter of the key K (as K is the 4th letter of the repeated key) to the 4th letter of the plaintext D : 3-10=-7+26= 19 , and to finish E and E so 4-4= 0 .

Each result is a number from 0 to 25 having a letter of the same rank in the alphabet that gives the cipher text.

Example: 19,24,16,19,0 becomes with 19:T, 24:Y, 16:Q, 19:T, 0:A, the cipher message TYQTA .

## How to decrypt Variant Beaufort cipher?

(German) Variant Beaufort cipher adds the message to the key, this is equivalent to encoding with Vigenere .

## How to recognize Variant Beaufort ciphertext?

A message encrypted with Variant Beaufort has an index of coincidence oscillating between 0.04 and 0.05, often smaller than the one of the language of the plain text.

Any reference to cheese is a clue ( Beaufort is the name of a cheese from Savoie, France)

## How to decipher Variant Beaufort without key?

Techniques to decode Beaufort are similar to the ones for Vigenere . dCode can analyze the text in order to find the probable key lengths ( Kasiski , etc.) and uses frequency analysis techniques to find the key.
