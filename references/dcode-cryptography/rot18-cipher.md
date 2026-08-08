# ROT-18 Cipher

> Source: [https://www.dcode.fr/rot18-cipher](https://www.dcode.fr/rot18-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is ROT-18? (Definition)

ROT-18 is the name given to 2 shift encryption methods, similar to the famous ROT-13 but using the 36 alphanumeric characters.

— Definition 1: Association of ROT-13 and ROT-5 (and 13+5=18), the letters are shifted by 13 (in the 26-letter alphabet ABCDEFGHIJKLMNOPQRSTUVWXYZ ) and the numbers by 5 (in the list 0123456789 )

— Definition 2: Use of a 36-character alphanumeric alphabet (26 letters and 10 numbers), the characters are then shifted by 18 positions.

These 2 definitions produce different and incompatible results.

## How to encrypt using ROT-18 cipher?

To encode by ROT-18 , take each character of the message to encode.

— ( ROT-13 + ROT-5 ): Replace the letters (A-Z) with those located 13 positions later in the looping alphabet and replace the numbers (0-9) with those located 5 positions later in the loop

Example: A becomes N , Z becomes M and 0 becomes 5 and 9 becomes 4

— ( ROT-18 ): Replace the characters (A-Z0-9) with those located 18 positions later in the 36-character alphanumeric alphabet: ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789

Non-alphanumeric characters remain unchanged (such as spaces, punctuation or symbols)

## How to decrypt ROT-18 cipher?

Decryption is the same as encryption (regardless of the definition used). ROT-18 is a reversible cipher. Decoding involves applying ROT-18 again to the encoded message.

## What are the variants of the ROT18 cipher?

ROT13 : Moves only letters 13 positions in the alphabet .

ROT13 .5: Another name for ROT18 .

ROT5 : Moves only numbers 5 positions.

ROT47 : Extends the shift to all printable ASCII characters, including symbols and punctuation.
