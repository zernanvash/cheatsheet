# Skip Cipher

> Source: [https://www.dcode.fr/skip-cipher](https://www.dcode.fr/skip-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is the Skip cipher? (Definition)

The skip cipher (or jump cipher) is a transposition cipher which reorders the letters of a message by extracting a letter every $ n $ characters (in other words, by jumping $ n $ characters or skipping $ n-1 $).

## How to encrypt using Skip cipher?

Set the size of the skip $ s $, extract the first letter of the message, then make jumps of $ s $ characters. When the end of the message is reached, go back at the beginning (loop).

Example: The message DCODE is encrypted with a jump/skip value of $ 3 $ and starting with the first letter: D then $ 3 $ further D then, at the end of the message, continue counting back at first to get C , then E , then go back to the beginning one last time for the last letter O . The encrypted message is DDCEO

Another method (with the identical result) is to use an infinite series of contiguous messages and to extract the characters by jump of $ s $. So all characters in position position $ 1 \mod s $ (Another way to look at it is to consider all multiples of $ s $ with indexing starting at 0)

Example: DCODE becomes by this method and jumps of $ 3 $: DDCEO DCODEDCODEDCO… D--D--C--E--O

DCODEDCODEDCO… D--D--C--E--O

For encryption to work, it is necessary to use a jump value that is a number coprime with the length of the message (see below).

## How to decrypt using Skip/Jump cipher?

Decryption requires knowledge of the $ s $ value of the jump.

Step 1: Create an empty array numbered from $ 0 $ to $ N-1 $ with $ N $ the length of the message.

Step 2: take the $ i $-th letter of the encrypted message and place it in the array in $ (i-1) \times s \mod N $

The plain message is the contents of the array after placing the $ N $ letters of the message.

Example: Decrypt the message DDCEO (5 letters) coded with a jump of $ 3 $ Step 1: create the table: [0][1][2][3][4] Step 2: the letter D in position $ 1 $ of the message is placed in position $ (1-1) \times 3 = 0 $ in the table: [D][_][_][_][_] Step 2: the letter D in position $ 2 $ of the message is placed in position $ (2-1) \times 3 = 3 $ in the table:' [D][_][_][D][_]' etc. until [D][C][O][D][E] which is the plain message.

## What are possible skip/jump values?

In order for encryption to work, the jump must be a coprime number with $ N $ (the number of characters in the message), that is, it does not share any divisor , otherwise the encryption will loop on itself and an encrypted message will never contain all the letters of the plain message.

Example: SKIP (length $ 4 $) can not be encrypted with a value like $ 2 $ ($ 2 $ and $ 4 $ are not coprime ) otherwise the encrypted message would be SISI (the loop would be partial and the letters' K and P 'will never appear)

## How to recognize a Skip ciphertext?

The encrypted message contains the same letters as the plaintext, but reordered (property of transposition cipher), the coincidence index of the skip encryption is identical to the plain message.

The first letter of the encrypted message is the first letter of the message if the starting position is 1.

## How to decipher Skip without Skip value?

Use the proposed Bruteforce search function on dCode that will attempt all possible jump values (integers coprime with N the length of the text)

For a message of length $ N $, this amounts to testing all $ s $ such that $ \text{gcd}(s, N) = 1 $, so approximately $ \varphi(N) $ trials (see the Euler totient ).

## What are the variants of the Skip cipher?

The starting position of the cipher can be changed, starting at $ i $ the message is slightly modified.

Taking punctuation into account greatly affects the message (but complicates manual encryption / decryption), it is recommended to ignore spaces or punctuation and keep only alphanumeric characters.
