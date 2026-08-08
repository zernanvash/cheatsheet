# Beaufort Cipher

> Source: [https://www.dcode.fr/beaufort-cipher](https://www.dcode.fr/beaufort-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is the Beaufort number? (Definition)

The Beaufort cipher is a polyalphabetic encryption system very similar to the Vigenère cipher , but based on a different operation: instead of adding the key to the plaintext, the plaintext is subtracted from the key.

## How to encrypt using Beaufort cipher?

Encryption is a variant of the Vigenere cipher , it uses a key (and an alphabet).

Example: Encrypt the plain text DCODE with the key KEY and the latin alphabet ABCDEFGHIJKLMNOPQRSTUVWXYZ

Match each letter of the alphabet to its rank, starting from 0. A corresponds to 0, B to 1, and so on up to Z which corresponds to 25.

Example: DCODE corresponds to 3,2,14,3,4 and KEY to 10,4,24 : Letter D C O D E Value 3 2 14 3 4

Letter D C O D E Value 3 2 14 3 4

Encryption consists in subtracting the plain text to the key. Calculation is made letter after letter ( subtraction of letters values in the alphabet).

If the result is negative, simply add 26, the length of the alphabet, to bring it back into a positive range.

The key is repeated as necessary in order that it fits the length of the plain text: KEYKEYKEYK…

Example: Subtract the first letter of the plain message D (=3) to the first letter of the key K (=10) : 10-3= 7 . Keep this result and continue with the next letters: the second letter of the plain message C and the second letter ot the key E : 4-2= 2 . Keep going with the third letters O and Y : 24-14= 10 . At the 4th step, at the end of the key, repeat it (or go to the beginning, its the same), subtract the 4th letter of the plaintext D to the first letter of the key K (where K is the 4th letter of the key if it has been repeated) : 10-3= 7 , and to finish E and E so 4-4= 0 .

Each result is a number between 0 and 25, to which a correspondence with a letter of the same rank in the alphabet get the cipher text.

Example: 7,2,10,7,0 becomes with 7:H, 2:C, 10:K, 7:H, 0:A, the cipher message HCKHA .

## How to decrypt Beaufort cipher?

The Beaufort cipher has for particularity that the decryption is identical to the encryption: subtract the cipher message to the key.

## How to recognize a Beaufort ciphertext?

The ciphered message has an indice of coincidence between 0.04 and 0.05, generally smaller than the one of the language of the plain text.

Beaufort is a French town in Savoie, known for its cheese, any reference to these elements can be a clue.

## How to decipher Beaufort without key?

Techniques for Beaufort automatic decryption are similar to techniques for Vigenere ( frequency analysis , probable key lengths, Kasiski method, etc.) to find the key.

## What are the variants of the Beaufort cipher?

Beaufort is already a variant of Vigenere . Where Vigenere adds the message to the key, Beaufort subtract the message to the key.

The German variant for Beaufort subtract the key to the message.

## When was Beaufort invented?

Sir Francis Beaufort , british amiral made this method published after his death by its brother in 1857. However, some writings indicate that this variant was known since 1710.
