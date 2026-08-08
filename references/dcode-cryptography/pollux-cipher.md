# Pollux Cipher

> Source: [https://www.dcode.fr/pollux-cipher](https://www.dcode.fr/pollux-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is the Pollux cipher? (Definition)

The Pollux cipher uses Morse code and a tomogrammic overcipher that replaces the dashes and dots of Morse code with alphanumeric characters.

## How to encrypt using Pollux cipher?

The plain message is first encoded in Morse, then the 3 Morse symbols (Dot, Dash and Space) are encoded via a predefined correspondence table.

Example: Dot (.) 0,4,7 Dash (-) 1,5,8 Space ( ) 2,3,6,9

Dot (.) 0,4,7 Dash (-) 1,5,8 Space ( ) 2,3,6,9

Example: Dot (.) 0378AEFMOPQXYZ Dash (-) 145BCGJNRTW Space ( ) 269DHIKLSUV

Dot (.) 0378AEFMOPQXYZ Dash (-) 145BCGJNRTW Space ( ) 269DHIKLSUV

Example: Encrypt CASTOR by writing it in Morse then transcode: Plaintext C A S T O R Morse code -.-. .- ... - - - .-. Encrypted text 4PGM9F1VQEMHCUB1B28BP

Plaintext C A S T O R Morse code -.-. .- ... - - - .-. Encrypted text 4PGM9F1VQEMHCUB1B28BP

The character is randomly selected from the list of possible characters.

## How to decrypt Pollux cipher?

Pollux decryption requires the knowledge of the correspondence between the numeric / alphanumeric characters and the dashes / points / spaces from the Morse code .

Example: Decrypt 78559590317270898307655205347035412184970 from the table Dot (.) 0,4,7 Dash (-) 1,5,8 Space ( ) 2,3,6,9

Dot (.) 0,4,7 Dash (-) 1,5,8 Space ( ) 2,3,6,9

The Morse code is reconstructed and can be translated into plain text.

Example: The corresponding Morse code is -... . - .- / --. . -- .. -. --- .-. ..- -- and the plain message is 'BETA GEMINORUM' (the scientific name of the Pollux star)

## How to decode Pollux without the correspondences?

Decoding a Pollux message without a Morse character-to-symbol correspondence table is extremely difficult, but not impossible.

It is possible to use a probabilistic approach called MCMC (Monte Carlo Markov Chain ). This method does not attempt to test all possible correspondences (which would be practically impossible), but rather to progressively explore the most likely configurations using a random optimization process.

— Starting from an initial (and often random) correspondence between the ciphertext and the Morse symbols.

— Decode the text according to this correspondence and evaluate the plausibility of the result (letter frequency, consistent words, etc.).

— Modify the correspondence slightly (by swapping a few symbols), re-evaluate the result, and if it is better, keep it; otherwise, try another modification.

By repeating this process thousands of times, the system converges towards the most plausible correspondence and thus towards the plaintext.

dCode applies this method but it does not always guarantee the exact solution (especially if the message is less than a hundred characters and the calculation time is limited), but it often allows to find at least a text close to the original message.

## How to recognize Pollux ciphertext?

A Pollux encrypted message will have a minimum coincidence index (due to polygrammic encrption and the characters chosen randomly). Cryptanalysis is therefore difficult.

Morse code does not usually have two consecutive spaces, and it is rare to find long sequences of dots or dashes. Also the text should not start with space because the first space character should be in position 2, 3, 4 or even 5.

Any reference to mythology, Dioscuri (Castor and Pollux ) is a clue.

Any reference to the Manège Enchanté (French TV series, with Pollux the dog) is a clue.

## When was Pollux cipher invented?

The Pollux cipher was popularized in some recreational cryptography publications in the 20th century. Its exact authorship remains unknown.
