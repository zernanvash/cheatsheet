# Scytale Cipher

> Source: [https://www.dcode.fr/scytale-cipher](https://www.dcode.fr/scytale-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is a scytale? (Definition)

A scytale is a transposition cipher used in ancient Greece, particularly in Sparta. It consists of a cylindrical rod around which a ribbon (often made of leather or parchment) is wound.

The message is written along the rod, following the spiral formed by the ribbon. Once the ribbon is unwound, the letters appear in a different order: the text becomes unintelligible without a rod of the same diameter.

The cipher known as the Caesar box has a different design but produces the exact same encrypted message, the method is also called rectangular transposition .

## How to encrypt using a Scytale?

Scytale Encryption uses a cylinder and a band characterized by its number of turns L (height) of the band around the cylinder of width/wideness (l).

Example: Code DCODE with a band L=3 .

The message is written along the cylinder, one letter per band, and when the end is reached, go to a new line.

If needed, complete the last row with another character, e.g. X or _ .

Example: DCO DE_

DCO DE_

The ciphered message is the band unrolled, (i.e the message read by column).

Example: The cipher text is DDCEO_

## How to decrypt a Scytale ciphertext?

Scytale Decryption requires to know the number N of letters by turn of the band (the size of the cylinder), or L the number of turns around the cylinder.

Example: The ciphertext is DDCEO_ (6-character long) and the band is L=3 , then N=2 (because 6/3=2).

Write the message on the band and wraps the band around the cylinder (of correct size) and the plain text should appear.

Example: DCO DE_ the original plain text is DCODE.

DCO DE_

Remove the final filler character if necessary.

## How to wrap the paper band?

To make a scytale , wind a strip of paper or parchment in a regular spiral around a cylinder (straight rod, tool handle, rigid tube).

The spirals must be close together and not overlap. The diameter of the cylinder is key: a cylinder of a different diameter will produce a different arrangement of the letters.

## What is the Plutarch's staff?

The Plutarch's staff is another name for the scytale . The technique is described by the Greek philosopher Plutarch in his historical writings, notably in Parallel Lives .

He is not necessarily the inventor, but one of the main ancient sources describing this technique used by the Spartans.

## How to recognize Scytale ciphertext?

The coincidence index is equal to the one of the original text (as it is a transposition cipher).

The message length should not be a prime number, but should have several divisors (including N the number of letters per ribbon turn and L the number of ribbon turns)

Any synonym of stick, rod, cane, cylinder, whorl, reel, roll, etc. is a clue.

The plutarch's staff is the name given to an album of Blake and Mortimer.

Any references to Greece, Sparta or the Spartans are clues.

Skytale is the direct Greek transliteration for skutalè

The Greek general Lysander and the ephors (Spartan magistrates) are described by Plutarch as users of scytales.

## How to decipher Scytale without the size?

One can crack Scytale by testing all possible size of the rectangle.

For a message of length M , the only possible dimensions are the pairs of factors L and N such that L x N = M.

An attacker would therefore have to try each divisor of M and analyze whether the resulting text is intelligible.

## When was Scytale invented?

The scytale is believed to have been used in Sparta between the 8th and 5th centuries BC, although written sources are later (the technique is described in the 1st century AD by Plutarch).

The exact date of its invention remains unknown, but its use is generally associated with the Greek Classical period.
