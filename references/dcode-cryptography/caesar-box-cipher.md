# Caesar Box Cipher

> Source: [https://www.dcode.fr/caesar-box-cipher](https://www.dcode.fr/caesar-box-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What it the Caesar Box cipher? (Definition)

Caesar Box is a transposition cipher used in the Roman Empire, in which letters of the message are written in rows in a square (or a rectangle) and then, read by column.

## How to encrypt using Caesar Box cipher?

To encode a message with Caesar's Box (Encryption Principle):

— Determine the size of the square (or the lengths of the sides of the rectangle). For a square, take the square root of the total number of characters.

NB: In practice, only the width of the square or rectangle matters (because it determines the number of columns)

Example: Encrypt the message DCODE in a rectangle of width 3

— Fill the square row by row with the letters of the message. If the number of characters is not a perfect square, add padding characters to complete.

Example: DCODE is cut every 3 characters and forms a rectangle (adding the character _ ): D C O D E _

D C O D E _

— Read the text column by column to form the encrypted text.

Example: The encrypted message is therefore DDCEO_

## How to decrypt Caesar Box cipher?

Deciphering Caesar's Box is done in 3 steps: (Deciphering principle)

— Know or determine the size of the square/rectangle.

Example: The encrypted message CSAAER is 6 characters long, 6 is not a perfect square number, so the message was encrypted in a 3x2 (or 2x3) rectangle.

— Fill the square column by column with the encrypted text.

Example: Writing in columns gives C A E S A R

C A E S A R

— Read the message line by line to find the original text

Example: The plain message is CAESAR .

## How to recognize Caesar Box ciphertext?

Caesar's box is a transposition cipher, its coincidence index is the same as that of the plaintext.

If a square grid is used, then the length of the message is a perfect square (4, 16, 25, 36, 49, 64, 72, 100, 121, 144, etc.)

This cipher appears in many movies or books like in Journey to the Center of the Earth by Jules Verne (cryptogram by Arne Saknussemm), etc.

When a square grid is used the encryption and decryption functions are identical.

## How to decipher Caesar Box without the size?

dCode's Brute-force function will determine the possible sizes of the square/rectangle based on the length of the message and attempt to find the plain message.

If the message has a perfect square number of characters, taking the root of it allows you to deduce the size of the square.

## What are the variants of the Caesar Box cipher?

Scytale is another name for this cipher ( scytale is a parchment/ribbon).

It is possible to encrypt a message that contains spaces or punctuation, but it is important to note the possible presence of multiple spaces by making them distinct.

Matrix transposition is the mathematical operation corresponding to this cipher.

## When was Caesar Box invented?

This encryption is identical to that of the scytale cipher, which have appeared in Greece (Sparta), between the 10th and 7th centuries B.C., a long time before romans and Caesar (Caius Iulius).
