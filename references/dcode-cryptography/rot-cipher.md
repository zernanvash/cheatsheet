# ROT Cipher

> Source: [https://www.dcode.fr/rot-cipher](https://www.dcode.fr/rot-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is Rot cipher? (Definition)

The ROT cipher (or Rot-N), short for Rotation , is a type of shift/rotation substitution encryption which consists of replacing each letter of a message with another located a little further (exactly N letters further) in the alphabet.

ROT is a basic cryptography method, often used for learning purposes. ROT is the basis of the famous Caesar cipher and its many variants modifying the shift.

The most popular variant is the ROT13 which has the advantage of being reversible with our 26 letters alphabet (the encryption or decryption operations are identical because 13 is half of 26).

## How to encrypt using Rot cipher?

To encode a message with the ROT cipher , the user chooses a number, usually between 1 and 25 (because there are 26 positions in the alphabet ), which represents the offset.

Then, each letter in the message is moved that number of positions to the right in the alphabet . If the offset exceeds the letter Z , it starts at the beginning of the (circular) alphabet.

Spaces, numbers, and non-alphabetic characters generally remain unchanged (accents are removed).

Plain Alphabet ABCDEFGHIJKLMNOPQRSTUVWXYZ Cipher Alphabet Shift/Rotation of 1 BCDEFGHIJKLMNOPQRSTUVWXYZA Cipher Alphabet Shift/Rotation of 2 CDEFGHIJKLMNOPQRSTUVWXYZAB … … Cipher Alphabet Shift/Rotation of 13 NOPQRSTUVWXYZABCDEFGHIJKLM … …

Plain Alphabet ABCDEFGHIJKLMNOPQRSTUVWXYZ Cipher Alphabet Shift/Rotation of 1 BCDEFGHIJKLMNOPQRSTUVWXYZA Cipher Alphabet Shift/Rotation of 2 CDEFGHIJKLMNOPQRSTUVWXYZAB … … Cipher Alphabet Shift/Rotation of 13 NOPQRSTUVWXYZABCDEFGHIJKLM … …

Example: The message ROTATION coded on the alphabet ABCDEFGHIJKLMNOPQRSTUVWXYZ with an offset of N=13 , gives the encrypted message EBGNGVBA .

Mathematically, the transformation of a message by ROT follows the formula C = (P + N) mod 26 where P is the position of the plaintext letter in the alphabet, N the chosen offset, and C the new position of the ciphertext letter in the alphabet.

## How to decrypt with Rot cipher?

Deciphering Rot is very similar (or sometimes identical) to encryption, with a shift of the alphabet in the other direction.

The classic ROT cipher is extremely vulnerable to brute force attacks, as there are only 25 possible combinations to test.

From a message and an alphabet (or a supposed alphabet), it is possible to test all rotations by bruteforce (as many tests as there are characters in the alphabet) in order to find the plain message.

## What are rot variants?

A variant of Rot consists of modifying the alphabet used, which may be different from the 26 characters (A to Z).

The best known are ROT13 and ROT47 but any offset and any alphabet can be considered: Shift Name Remarks 1 Rot1/Rot-1 Minimal shift of 1 letter 2 Rot2/Rot-2 3 Rot3/Rot-3 Caesar Cipher (default usual shift) 4 Rot4/Rot-4 5 Rot5/Rot-5 Reversible for the 10 digits 6 Rot6/Rot-6 7 Rot7/Rot-7 8 Rot8/Rot-8 9 Rot9/Rot-9 10 Rot10/Rot-10 11 Rot11/Rot-11 12 Rot12/Rot-12 13 Rot13/Rot-13 Reversible for our 26-letter alphabet 14 Rot14/Rot-14 15 Rot15/Rot-15 16 Rot16/Rot-16 Reversible for base32 encoding 17 Rot17/Rot-17 18 Rot18/Rot-18 Reversible for an alphanumeric alphabet of 36 characters (26 letters + 10 digits) 19 Rot19/Rot-19 20 Rot20/Rot-20 21 Rot21/Rot-21 22 Rot22/Rot-22 23 Rot23/Rot-23 24 Rot24/Rot-24 25 Rot25/Rot-25 Reverse 1 letter shift 26 Rot26/Rot-26 Identity transformation (no change) for our 26-letter alphabet 31 Rot31/Rot-31 Reversible for an case-sensitive alphanumeric 62-chars alphabet (26 uppercase + 26 lowercase + 10 digits) 32 Rot32/Rot-32 Reversible for base64 encoding 47 Rot47/Rot-47 Reversible for the 94 ASCII printable characters

Shift Name Remarks 1 Rot1/Rot-1 Minimal shift of 1 letter 2 Rot2/Rot-2 3 Rot3/Rot-3 Caesar Cipher (default usual shift) 4 Rot4/Rot-4 5 Rot5/Rot-5 Reversible for the 10 digits 6 Rot6/Rot-6 7 Rot7/Rot-7 8 Rot8/Rot-8 9 Rot9/Rot-9 10 Rot10/Rot-10 11 Rot11/Rot-11 12 Rot12/Rot-12 13 Rot13/Rot-13 Reversible for our 26-letter alphabet 14 Rot14/Rot-14 15 Rot15/Rot-15 16 Rot16/Rot-16 Reversible for base32 encoding 17 Rot17/Rot-17 18 Rot18/Rot-18 Reversible for an alphanumeric alphabet of 36 characters (26 letters + 10 digits) 19 Rot19/Rot-19 20 Rot20/Rot-20 21 Rot21/Rot-21 22 Rot22/Rot-22 23 Rot23/Rot-23 24 Rot24/Rot-24 25 Rot25/Rot-25 Reverse 1 letter shift 26 Rot26/Rot-26 Identity transformation (no change) for our 26-letter alphabet 31 Rot31/Rot-31 Reversible for an case-sensitive alphanumeric 62-chars alphabet (26 uppercase + 26 lowercase + 10 digits) 32 Rot32/Rot-32 Reversible for base64 encoding 47 Rot47/Rot-47 Reversible for the 94 ASCII printable characters

## Why is the ROT cipher used?

The ROT cipher is primarily used for educational purposes to illustrate basic cryptography concepts.

It's also often used in games and puzzles, especially for clues.

Forums and social media use it to hide spoilers.

Historically, the Caesar code was used in antiquity for military communications purposes.
