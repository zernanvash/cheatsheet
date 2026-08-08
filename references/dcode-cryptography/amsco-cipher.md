# AMSCO Cipher

> Source: [https://www.dcode.fr/amsco-cipher](https://www.dcode.fr/amsco-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is AMSCO cipher? (Definition)

AMSCO is a (incomplete) columnar transposition cipher performing a permutation of an alternation of bigrams and unigrams of the plaintext.

## How to encrypt using AMSCO cipher?

AMSCO Encryption consists in writing a text in a grid according to a cutting sequence then use a permutation key to switch columns.

Example: Encrypt the message DCODEAMSCO , with a cutting sequence 1,2 (alternation of 1 letter then 2 letters in the grid, both in rows and in columns)

Select a permutation key (of length L), and write the message in lines, cut over L columns.

Example: If the key is KEY (equivalent to 2,1,3 ) of length 3, then write the message over 3 columns: \ 1 2 3 D CO D EA M SC O

\ 1 2 3 D CO D EA M SC O

Read the grid in columns, in the order of the key (this reading serves as permutation).

Example: Column 2 ( COM ) then 1 ( DEAO ), and the 3 ( DSC ). The message is COMDEAODSC .

## How to decrypt AMSCO cipher?

AMSCO decryption requires knowledge of the permutation key (of length L) and the cutting sequence (usually 1,2 or 2,1 ).

Example: Decrypt the message COMDEAODSC (of 10-characters length) with the key KEY (equivalent to the permutation 2,1,3 ) of length 3, and cutting sequence 1.2 .

Create a table with L columns, in which the number of characters are noted in each cell (in respect to the cutting sequence and limited by the length of the message).

Example: 1,2 for 10 characters corresponds to (1+2+1+2+1+2+1+0+0 = 10) : \ 1 2 3 1 2 1 2 1 2 1 0 0

\ 1 2 3 1 2 1 2 1 2 1 0 0

Write the message in the table in columns following the order of the columns indicated by the key.

Example: Write CO , then M in column 2, then D , EA , O in column 1, then D , DC in column 3. This leads to the grid: \ 1 2 3 D CO D EA M SC O

\ 1 2 3 D CO D EA M SC O

The plain message is transcribed by reading the table in lines.

Example: Reading each lines gives the original plain text is DCODEAMSCO .

## How to correctly split the text into the grid?

The text must alternate sizes of cuts (even if the key size is even) which then should form diagonal sets:

Example: A grid of width 3, cut by (1,2): \ 1 2 3 1 2 1 2 1 2 1 2 1

\ 1 2 3 1 2 1 2 1 2 1 2 1

Example: A grid of width 3, cut by (2,1): \ 1 2 3 2 1 2 1 2 1 2 1 2

\ 1 2 3 2 1 2 1 2 1 2 1 2

Example: A grid of width 4, cut by (1,2): \ 1 2 3 4 1 2 1 2 2 1 2 1 1 2 1 2

\ 1 2 3 4 1 2 1 2 2 1 2 1 1 2 1 2

Example: A grid of width 3, cut by (3,2,1): \ 1 2 3 3 2 1 2 1 3 1 3 2

\ 1 2 3 3 2 1 2 1 3 1 3 2

No need to fill the grid with null letters if a cell is empty or incomplete.

## How to recognize AMSCO ciphertext?

The ciphered message is subjected to a single transposition , so it has an index of coincidence similar to the one of the plain text.

## How to decipher AMSCO without a key?

It is possible to try to infer the key length by analyzing bigrams obtained after writing in columns.

## What are the variants of the AMSCO cipher?

AMSCO is a variant of the classical transposition cipher. It adds the cut sequence that can be more complex than the usual 1,2 .

## When was AMSCO invented?

AMSCO dates from the 19th and bear the initials of its author A. M. Scott
