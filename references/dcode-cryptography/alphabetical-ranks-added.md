# Alphabetical Ranks Added

> Source: [https://www.dcode.fr/alphabetical-ranks-added](https://www.dcode.fr/alphabetical-ranks-added)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## How to encrypt using Added Alphabetical Rank A1Z26 cipher?

A1Z26 Added Encryption consists of adding each number (which represents the position of a letter of the alphabet) to the number preceding it. The sum obtained is the encrypted letter.

Example: ABC ( 1,2,3 ) is coded 1,(2+1)=3,(3+3)=6 so 1,3,6

Example: DCODE ( 4,3,15,4,5 ) becomes 4,(3+4)=7,(15+7)=22,(4+22)=26,(5+26)=31 so 4,7,22,26,31

## How to decrypt Added Alphabetical Rank cipher?

Decryption implies to subtract each number to the one that precedes to obtain new numbers that correspond to a substitution by classical alphabetical ranking.

Example: The encrypted message is 4,7,22,26,31

Subtract each value to one before (except for the first value).

Example: 4,7-4,22-7,26-22,31-26 gives 4,3,15,4,5

A substitution is carried out according to the rank in the alphabet .

Example: 4 = D , 3 = C , etc. The plain message is DCODE .

If the result of the subtraction is less than zero or greater than the number of letters in the alphabet, then it is possible to perform a modulo operation.

## How to recognize Added Alphabetical Rank ciphertext?

The message is composed of numbers which should mainly be increasing. (Each number must be larger than the previous one). Moreover, the difference between two numbers should ideally be between 1 and 26 (where 26 is the number of letters in the alphabet)
