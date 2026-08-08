# Chaocipher

> Source: [https://www.dcode.fr/chao-cipher](https://www.dcode.fr/chao-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is Chaocipher? (Definition)

The Chaocipher cipher is a dynamic polyalphabetic substitution cipher invented in 1918 by John F. Byrne. It relies on two circular alphabets (often represented as disks) that evolve after each letter is processed.

At each step, a letter from the plaintext is associated with a letter from the ciphertext according to the relative position of the two alphabets. These alphabets are then modified by a specific permutation. This mechanism makes the letter correspondence different at each iteration, introducing a quasi-chaotic behavior into the cipher.

## How to encrypt using Chaocipher?

Chaocipher encryption uses two rotating disks on which is written a custom alphabet (originally the 26 letters from A to Z using a deranged alphabet ).

The two disks are identical and linked with a kind of gearing (ratio 1:1), if a disk is turned clockwise, the other turns anti-clockwise.

Example: Encrypt DCODE using the two disks: CHAOBDEFGIJKLMNPQRSTUVWXYZ for the LEFT disk (cipher text) and CIPHERABDFGJKLMNOQSTUVWXYZ for the RIGHT disk (plain text)

The position 1 in each disk alphabet is called zenith and the opposite position on the disk, here 14, is called nadir .

For each letter to encrypt, make these 3 steps:

First step: read the cipher letter corresponding to the plain letter (at the intersection of the two disks or at the same rank in the alphabets)

Example: The plain letter D is in front of the cipher letter G .

Second step: make a special permutation of the LEFT disk. This operation is composed of 4 actions:

1. Make a rotation of the alphabet on order to set the cipher letter at the zenith (position 1)

Example: The alphabet becomes GIJKLMNPQRSTUVWXYZCHAOBDEF

2. Extract the letter in position zenith+1 (on the right of zénith) and leave the position empty

Example: Extraction of I . The alphabet becomes G.JKLMNPQRSTUVWXYZCHAOBDEF

3. Shift all letters from position zenith+2 until nadir (zenith+13) included by shifting them on the left

Example: The alphabet becomes GJKLMNPQRSTUV.WXYZCHAOBDEF

4. Insert the extracted letter at step 2 in the empty hole in position nadir (zenith+13)

Example: The alphabet becomes GJKLMNPQRSTUVIWXYZCHAOBDEF

Third step: make a special permutation of the RIGHT disk. This operation is composed of 4 actions:

1. Make a rotation of the alphabet in order to set the letter immediately to the right of the plain letter to the zenith (the plain letter is in position zenith-1).

Example: The alphabet becomes FGJKLMNOQSTUVWXYZCIPHERABD

2. Extract the letter in position zenith+2 and leave the position empty.

Example: Extraction of J . The alphabet becomes FG.KLMNOQSTUVWXYZCIPHERABD

3. Shift all letters from position zenith+3 until nadir (zenith+13) included by shifting them on the left

Example: The alphabet becomes FGKLMNOQSTUVW.XYZCIPHERABD

4. Insert the extracted letter at step 3 in the empty hole in position nadir (zenith+13).

Example: The alphabet becomes FGKLMNOQSTUVWJXYZCIPHERABD

The message is obtained after these steps.

Example: Here the cipher message is GZNDZ

## How to decrypt Chaocipher?

Decryption with Chaocipher follows the exact same steps as encryption.

The only difference is the initial read: you must locate the encrypted letter on the LEFT disk and read the corresponding letter on the RIGHT disk.

After each letter, the two alphabets are modified with the same permutations as during encryption.

## How to recognize Chaocipher ciphertext?

The Chaocipher cipher is difficult to recognize because it does not leave a simple statistical signature.

As it is a dynamic polyalphabetic cipher, the distribution of letters tends to approach a uniform distribution.

The index of coincidence is generally low.

## How to decipher Chaocipher without disks?

Deciphering a Chaocipher message without knowing the initial alphabets is extremely difficult.

The system introduces a strong dependency between each letter, which prevents the use of classic frequency analysis methods. In theory, an attack is possible if the user has a long text, knows the language used, and can test a large number of hypotheses.

## What are the variants of the Chaocipher cipher?

It is possible to modify the size of the alphabet (for example, to include numbers or symbols) or to adapt the permutation rules (positions of extractions and insertions).

## When Chaocipher was invented?

The Chaocipher was invented in 1918 by John F. Byrne. For several decades, its workings remained secret, with Byrne claiming it was unbreakable.

The algorithm was only publicly revealed in 2010, finally allowing its analysis by the scientific community. The Chaocipher is described in his book Silent Years here (affiliate link)
