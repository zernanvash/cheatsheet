# Gronsfeld Cipher

> Source: [https://www.dcode.fr/gronsfeld-cipher](https://www.dcode.fr/gronsfeld-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is the Gronsfeld cipher? (Definition)

The Gronsfeld cipher is a polyalphabetic encryption method based on a system of shifting the letters of the alphabet according to a numerical sequence called a key . This method is also called a multiple shift cipher. It is a variant of the Vigenère cipher , but with a key limited to digits (0-9) instead of letters.

## How to encrypt using Gronsfeld cipher?

The Gronsfeld cipher is identical to the Vigenère cipher , the only difference being that the key is numeric.

For each letter of the plain message,shift it (advance) in the alphabet by the corresponding key digit (repeat the key digits if necessary).

Example: To encrypt the message GRONSFELD with the key 1234 , add 1 to G or H (the letter 1 row after G is H in the alphabet), then add 2 to C or E (the letter 2 rows after C is E ), etc.

Plain letter G R O N S F E L D Key (repeated) 1 2 3 4 1 2 3 4 1 Cipher Letter H T R R T H H P E

Plain letter G R O N S F E L D Key (repeated) 1 2 3 4 1 2 3 4 1 Cipher Letter H T R R T H H P E

Example: The encrypted message is HTRRTHHPE .

## How to decrypt Gronsfeld cipher?

Gronsfeld decryption requires knowing the decryption key (and the alphabet used if it is not classical). Here again, Gronsfeld decryption is identical to Vigenere , but with a digital key.

For each letter in the encrypted message, shift it (backward) in the alphabet by the corresponding key digit (repeat the key digits if necessary).

Example: Decrypt the encrypted message EEREG with the key 123

Ciphertext Letter E E R E G Key (Repeated) 1 2 3 1 2 Decrypted Letter D C O D E

Ciphertext Letter E E R E G Key (Repeated) 1 2 3 1 2 Decrypted Letter D C O D E

Example: The plain message is then DCODE .

## How to recognize Gronsfeld ciphertext?

The message has an index of coincidence of about 0.04 to 0.05 (similar to Vigenere ).

Any number that can serve as a numeric key is a clue.

## How to decipher Gronsfeld without the key?

Cryptanalysis techniques used for Vigenere are also applicable to Gronsfeld .

These techniques also accelerated since the use of a numeric key limits the number of combinations (each character of the key has only 10 possibilities against 26 with Vigenere ).

## How many possible key combinations are there?

The number of possible key combinations depends on the length of the key. Each position of the key can be filled with one of the 10 digits (0 to 9). For a key of length N, there are 10^N combinations .

If the length of the key is not known, count all the key sizes from 1 to N.
