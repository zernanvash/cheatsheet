# PGP Word List

> Source: [https://www.dcode.fr/pgp-word-list](https://www.dcode.fr/pgp-word-list)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is PGP Word List? (Definition)

The PGP wordlist is a standardized set of words associated with each numeric value (from 0 to 255) used to verify and communicate cryptographic key fingerprints.

Sometimes called a biometric word list, it facilitates the vocal (or written) communication of these signatures by avoiding transcription errors due to confusion between numbers or letters.

## How to encode data with PGP list?

To encode data with a PGP wordlist, each byte of the data is converted into corresponding words from the PGP list.

The PGP wordlist was created to simplify the communication of PGP crypto keys in hexadecimal format, but the process applies to any binary message.

Each byte is associated with a specific word in 2 predefined lists. Each list is 256 words long (indexed from 00 to FF ).

The first list (called even) contains 2- syllable words, the second list (called odd) contains 3- syllable words so as not to confuse them. Here is an excerpt: Byte even word odd word 00 aardvark adroitness 01 absurd adviser 02 accrue aftermath . . . FF Zulu Yucatan

Byte even word odd word 00 aardvark adroitness 01 absurd adviser 02 accrue aftermath . . . FF Zulu Yucatan

Each even byte is encoded with the corresponding word in the even list, and each odd byte is encoded with the corresponding word in the odd list. (NB: the bytes are 0-indexed, the first one is in position 0, so it is encoded with the even list)

Example: DC,0D,33 is converted to sweatband,asteroid,chisel

## How to decode PGP words?

To decode PGP words, you do the reverse of encoding: convert each word from the PGP list into its corresponding byte (in hexadecimal form) in order to reconstruct the original data.

Example: sweatband corresponds to DC , asteroid to 0D , chisel to 33

## How to recognize words from the PGP list? (Identification)

PGP list words have a maximum length of 11 letters respectively (to be precise 9 letters for the even list, and 11 letters for the odd list).

Even list words have 2 syllables , odd list words have 3 syllables .

PGP list words are specially chosen to be easily distinguishable, even under difficult communication conditions.
