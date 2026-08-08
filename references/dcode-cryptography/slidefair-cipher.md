# Slidefair Cipher

> Source: [https://www.dcode.fr/slidefair-cipher](https://www.dcode.fr/slidefair-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## How to encrypt using Slidefair cipher?

Slidefair encryption uses an encryption key (as well as an alphabet) and is performed by bigrams (pairs of 2 letters).

Example: Encrypt MESSAGE with the key ABC , and the Latin alphabet ABCDEFGHIJKLMNOPQRSTUVWXYZ which generates this square (identical to Vigenère 's square)

Step 1: Break down the message into bigrams (numbered $ i $) and for each associate the $ i $ th letter of the key (repeated). If the message has an odd length, the last bigram must be completed by a letter, random or neutral.

For each bigram , perform the following steps:

Step 2: Locate in the table the column having as name the first letter of the bigram $ L_1 $.

Step 3: Locate in the table the row having as name the $ i $ th letter of the key $ L_2 $.

Step 4: Note the letter $ L_3 $ at the intersection of the column found in step 1 and the row found in step 2.

Step 5: Browse the row found in step 3 until finding the second letter of the bigram and note the letter $ L_4 $ of the name of the column found.

If $ L_3 $ and $ L_4 $ are on the same column, then replace $ L_3 $ and $ L_4 $ respectively with the letters which are immediately to the right of the letters $ L_1 $ and $ L_3 $.

The coded bigram is then formed by the letters $ L_3 $ and $ L_4 $, first noting the highest letter in the table.

Example: The encrypted message is EMRTECXE Plain Bigrams ME SS AG EX Key A B C A Letter $ L_1 $ M S A E Letter $ L_2 $ A B C A Letter $ L_3 $ M T C E Letter $ L_4 $ E R E X Cipher Bigrams EM RT EC XE

Plain Bigrams ME SS AG EX Key A B C A Letter $ L_1 $ M S A E Letter $ L_2 $ A B C A Letter $ L_3 $ M T C E Letter $ L_4 $ E R E X Cipher Bigrams EM RT EC XE

## How to decrypt Slidefair cipher?

The principle of Slidefair decryption is identical to encryption, except in the particular case where the two letters identified in the grid are on the same column, in this case instead of taking the letters directly to the right, take the letters directly to the left.

## How to recognize a Slidefair ciphertext?

Slidefair is made up of bigrams so has an even number of characters.

Slidefair has a low coincidence index because it is a polyalphabetic cipher.

## What are the variants of the Slidefair cipher?

Slidefair can have many variations, first of all with the use of a different table, which can be generated with a disordered alphabet , or which can be entirely random.

By default, the table is that of Vigenère , but all its variants ( Beaufort , etc.) are possible.

Slidefair can be considered as a variant of Playfair .
