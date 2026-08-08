# ROT-13 Cipher

> Source: [https://www.dcode.fr/rot-13-cipher](https://www.dcode.fr/rot-13-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is Rot-13? (Definition)

Rot-13 (short for Rotation 13 or Rotate by 13) is the name given to a mono-alphabetical substitution cipher which has the property of being reversible and very simple.

Combining the French/Latin alphabet of 26 letters and an offset of 13, Rot-13 replaces a letter with another located thirteen places further down the alphabet.

Rot-13 coding is popular to hide content because it is easily reversible, indeed, if it is applied twice, then the original message reappears.

This is a special case of the Caesar cipher (and more generally shift ciphers).

## How to encrypt using Rot-13?

From an alphabet, usually the classic 26-letter alphabet ABCDEFGHIJKLMNOPQRSTUVWXYZ , each letter is shifted by 13 positions in the English alphabet. Letters beyond Z return to the beginning of the alphabet (as if the alphabet were rotating on itself).

The correspondence table is: ABCDEFGHIJKLMNOPQRSTUVWXYZ NOPQRSTUVWXYZABCDEFGHIJKLM

ABCDEFGHIJKLMNOPQRSTUVWXYZ NOPQRSTUVWXYZABCDEFGHIJKLM

Example: DCODE is encrypted QPBQR with ROT-13

ROT13 applies only to the 26 unaccented letters of the Latin alphabet (A–Z). Accents are removed, numbers remain the same (unless ROT13 .5 is applied), and symbols are removed or ignored.

ROT13 is case-insensitive: uppercase and lowercase letters are transformed independently.

## How to decrypt a Rot-13 cipher?

Rot-13 decryption is identical to encryption, due to the reciprocal substituting alphabet used: NOPQRSTUVWXYZABCDEFGHIJKLM ABCDEFGHIJKLMNOPQRSTUVWXYZ

NOPQRSTUVWXYZABCDEFGHIJKLM ABCDEFGHIJKLMNOPQRSTUVWXYZ

Example: URYYB becomes HELLO.

NB: Rot-13 has the same function for encryption and decryption, it is said to be involutive . In other words, applying the ROT-13 Cipher twice on a text will return it to its original state.

## How to recognize ROT-13 ciphertext?

Frequency analysis shows a shift of 13 letters (The E is replaced by an R , which should be the most present letter).

A ROT13 encoded message has a coincidence index (a frequency distribution) identical to that of the plain text, because it is a simple substitution of letters.

The ROT13 code has been widely popularized on Usenet groups and discussion forums, as an anti-spoil method.

Any reference to Friday the 13th, the fear of the number 13 (triskaidekaphobia), the expression baker's dozen (meaning thirteen), the equations A=N or E=R or the three letters EBG (i.e. ROT shifted by 13) are clues.

## What are the variants of the Rot-13 cipher?

Rot-13 is in fact a Caesar cipher with a shift of thirteen. As this code only works with letters, it is possible to add the ROT5 to it for the digits (in this case it is sometimes called ROT13 .5) or even to use the ROT47 to manage all the ASCII characters.

## What is the particularity of the ROT13 Cipher?

An offset of 13 allows the encryption to be reversible. The encryption and decryption method are identical. Applying 2 consecutive encryptions (2 shifts of 13) heads to find the original text.

NB: ROT13 does not provide any cryptographic security; it is used only to temporarily hide text.

## Why does 2 encryption with ROT13 cancel each other?

Applying 2 shifts of 13 represents a shift of 26, and for the Latin alphabet of 26 letters, this amounts to shifting all the letters to their starting point, so in the end, not undergoing any transformation.

ROT13 ( ROT13 (letter)) = letter

## What is the difference between ROT13 and Caesar cipher?

The ROT13 cipher does not introduce any new principle compared to the Caesar cipher . It is a special case of it, setting the shift to exactly 13 letters.

## Is there an equivalent for other alphabets (Greek, Cyrillic, etc.)?

The ROT13 principle can be generalized to any alphabet, as long as it is an ordered set of symbols.

However, there is no universal standard for alphabets other than the 26-letter Latin alphabet.

Example: The Greek alphabet (24 letters) would have an equivalent of ROT12

Example: The Cyrillic alphabet (33 letters) would have no equivalent because 33 is an odd number.
