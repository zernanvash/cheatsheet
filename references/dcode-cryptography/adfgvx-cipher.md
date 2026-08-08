# ADFGVX Cipher

> Source: [https://www.dcode.fr/adfgvx-cipher](https://www.dcode.fr/adfgvx-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is the ADFGVX cipher? (Definition)

ADFGVX is a German encryption system dating from the First World War using a grid and the letters A,D,F,G,V,X before subjecting the ciphertext to column transposition .

## How to encrypt using ADFGVX cipher?

The ADFGVX encryption uses a 6x6 square grid of 36 distinct characters (often generated via a keyword allowing to shuffle the 26 letters of the latin alphabet and the 10 digits from 0 to 9).

Rows and columns are named, from top to bottom and from left to right, by the letters A , D , F , G , V and X in order for the letters of the grid to be located by a coordinate (row, column).

Example: A default ADFGVX grid (without keyword), such as A = (A,A) , Z = (V,D) etc. \ A D F G V X A A B C D E F D G H I J K L F M N O P Q R G S T U V W X V Y Z 0 1 2 3 X 4 5 6 7 8 9

\ A D F G V X A A B C D E F D G H I J K L F M N O P Q R G S T U V W X V Y Z 0 1 2 3 X 4 5 6 7 8 9

Perform a substitution by bigrams by replacing each letter of the message by the corresponding pair of coordinates ( bigram ).

Example: BERLIN becomes AD,AV,FX,DX,DF,FD

This message will get another encryption by columnar transposition . The transposition uses a permutation key/keyphrase, usually based on a keyword. This can be found it by rearranging its letters in alphabetic order.

Two same letters are ranked in order of appearance, but if possible avoid duplicates letters in the keyphrase as this can lead to encryption/decryption ambiguities.

Example: The keyword CODE gives the transposition 1,3,4,2 because C(1),O(2),D(3),E(4) ranks alphabetically C(1),D(3),E(4),O(2) i.e. columns 1,3,4,2

The message is written by rows in a table whose width is the key size.

Any empty cells in the last row are sometimes filled with X (or other letters) to simplify manual decryption.

Example: C(1) O(2) D(3) E(4) A D A V F X D X D F F D

C(1) O(2) D(3) E(4) A D A V F X D X D F F D

Columns are rearranged such as the permutation key.

Example: After transposition 1,3,4,2 (The 2nd column O(2) is placed at the end) C(1) D(3) E(4) O(2) A A V D F D X X D F D F

C(1) D(3) E(4) O(2) A A V D F D X X D F D F

The ADFGVX final ciphertext is made by reading the letters of the table by columns starting from top to bottom and from left to right.

Example: Final encrypted message is AFDADFVXDDXF

The coded message is usually transmitted in Morse code to the recipient.

## How to decrypt ADFGVX cipher?

The ADFGVX decryption process requires a key and a grid.

Example: The cipher text is AD,AX,FV,FF,GF,AX and the keyword is KEY (that correspond to permutation K(1),E(2),Y(3) => E(2),K(1),Y(3) => 2,1,3 )

The ciphered message is then written from top to bottom and from left to right in a table with $ n $ columns where $ n $ is the length of the key. Columns are named according to the letters of the key, rearranged in alphabetic order.

Example: E(2) K(1) Y(3) A F G D V F A F A X F

E(2) K(1) Y(3) A F G D V F A F A X F

If during the encryption, the last row was not completed by X , take this into account to fill in the cells of the last row.

The table gets a permutation of its columns according to the permutation key in order to get back the original order of the keyword's letters.

Example: K(1) E(2) Y(3) F A G V D F F A A F

K(1) E(2) Y(3) F A G V D F F A A F

Reading the table by row gives the intermediate message.

Example: FAGVDFFAAFXX .

For each bigrams , replace it with the corresponding letter with coordinates (row, column) in the grid to get the plain text message.

Example: \ A D F G V X A A Z E R T Y D U I O P Q S F D F G H J K G L M W X C V V B N 0 1 2 3 X 4 5 6 7 8 9

\ A D F G V X A A Z E R T Y D U I O P Q S F D F G H J K G L M W X C V V B N 0 1 2 3 X 4 5 6 7 8 9

Example: FA = row F, column A = D then GV = C, etc. The original plain text is DCODE.

## How to recognize an ADFGVX ciphertext?

The ciphertext must contain only 6 distinct characters: A, D, F, G, V and X.

If the array is completed during encryption, the message will have a number of characters which is a multiple of the length of the permutation key.

## How to recognize a non-permuted text?

If the ciphertext hasn't be permuted, the text is a bigrammic substitution. After a substitution by a random alphabet , the text should have a the same index of coincidence as the plain text.

## How to decipher ADFGVX without key for permutation?

One can crack ADFGVX and find the permutation order without knowing the key by bruteforcing all possible permutation. Use the Permutation Brute-force button.

## How to decipher ADFGVX without grid?

One can crack ADFGVX and find the substitution grid by making a alphanumeric replacement of the bigrams resulting from the permutations. Use dCode's tool for mono-alphabetic substitution .

## How to decipher ADFGVX without key nor grid?

One can crack ADFGVX without the key nor the grid by finding first the permutation (see below) and then do an alphabetical substitution .

## Why the letters ADFGVX?

The letters A, D, F, G, V and X have been selected because their equivalent in morse code are very distinguishable, his prevent transmission error by radio

## When ADFGVX have been used?

ADFGVX cipher have been introduced at the end of the First World War (from 1917) by Fritz Nebel. He have been used on the 5th of March 1918 during the german attack of Paris, it was using an ADFGX version (with the letters A, D, F, G and X only).

## What is the GEDEFU 18?

GEDEFU 18 for GEheimschrift DEr FUnker 18, which can be translated in radio-operators' cipher 18 is the old name of ADFGVX cipher.

## What is ADFGX cipher?

ADFGX is an ancestor of ADFGVX , a variant using a 5x5 square, on the base of the Polybius square cipher.

## Who did crack ADFGVX cipher?

The crack is attributed to Georges-Jean Painvin. Among the deciphered messages, one text was nicknamed The radiogram of the victory because it allowed France to win a battle in June 1918.

## When ADFGVX have been cracked?

George-Jean Painvin deciphered a first message in June 1918.

## What is the Roitelet Theorem?

The theorem of Roitelet is a novel by Frédéric Cathala here (affiliate link) which has as protagonist a spy during the first world war having messages encrypted with ADFGVX .
