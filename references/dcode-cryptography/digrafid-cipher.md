# Digrafid Cipher

> Source: [https://www.dcode.fr/digrafid-cipher](https://www.dcode.fr/digrafid-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## How to encrypt using Digrafid cipher?

Digrafid encryption uses 2 grids (of 3x9 and 9x3) with 27 characters: ABCDEFGHIJKLMNOPQRSTUVWXYZ# (the # symbol is added to the alphabet).

Example: Encrypt DCODE with two alphabetical grids with identical content: ABCDEFGHIJKLMNOPQRSTUVWXYZ# , the first (1) is horizontal and the second (2) vertical and are connected by a 3rd grid (3) numeric 3x3 as follows: (1) \ 1 2 3 4 5 6 7 8 9 1 A B C D E F G H I 2 J K L M N O P Q R 3 S T U V W X Y Z # (3) \ 1 2 3 1 1 2 3 2 4 5 6 3 7 8 9 \ 1 2 3 1 A B C 2 D E F 3 G H I 4 J K L 5 M N O 6 P Q R 7 S T U 8 V W X 9 Y Z # (2)

(1) \ 1 2 3 4 5 6 7 8 9 1 A B C D E F G H I 2 J K L M N O P Q R 3 S T U V W X Y Z # (3) \ 1 2 3 1 1 2 3 2 4 5 6 3 7 8 9 \ 1 2 3 1 A B C 2 D E F 3 G H I 4 J K L 5 M N O 6 P Q R 7 S T U 8 V W X 9 Y Z # (2)

\ 1 2 3 4 5 6 7 8 9 1 A B C D E F G H I 2 J K L M N O P Q R 3 S T U V W X Y Z #

\ 1 2 3 1 1 2 3 2 4 5 6 3 7 8 9

\ 1 2 3 1 A B C 2 D E F 3 G H I 4 J K L 5 M N O 6 P Q R 7 S T U 8 V W X 9 Y Z #

Split the plain message into blocks of 6 and make 3 bigrams . If the message to be encrypted has a non-multiple length of 6, symbols are added (usually # ).

Example: The length of the plain text DCODE (5 letters) is not multiple of 6 , add # at the end: DCODE# and the cut in bigrams to get DC,OD,E#

For each bigram consisting of the letters L1 and L2 , carry out the following operations:

1) Write down 3 numbers:

— Mark in the grid 1 the column number of the letter L1 .

— Mark in the grid 3 the intersection number of the line L1 in the grid 1 and the column of L2 in the grid 2 .

— Mark in grid 2 the line number of the letter L2 .

Example: For the first bigram DC , in grid 1, the letter D is in position (1,4) (line 1, column 4). In grid 2, the letter C is in position (1,3) (line 1, column 3). The intersection of the two letters in the grid 3 is thus in position (1,3) (line 1, column 3) is the number 3 . 4,3,1 are the 3 digits necessary for the following encryption: (4: column of the letter D in the grid 1 , 3 number of the grid 3 , and 1 line of the letter C in the grid 3 ) . In the same way OD and E# respectively correspond to triplets 6,4,2 and 5,3,9 .

2) Write the 3 groups of 3 digits obtained in the block of 6 horizontally one below the other.

Example: 4 3 1 6 4 2 5 3 9

4 3 1 6 4 2 5 3 9

3) Then read vertically (in columns) to obtain 3 new 3-digit numbers.

Example: Reading in column gives 3 new triplets: 4,6,5 , 3,4,3 , 1,2,9 .

4) With the numbers x,y,z of each triplet, locate

— The position of y in grid 3 (line L , column C )

— The letter in line position L , column x in grid 1

— The letter in line position z , column C in grid 2

The 2 letters obtained are the numerical letters for the bigram

Example: With the first triplet 4,6,5 , mark 6 in grid 3 which is on line 2 and column 3 . The letter in grid 1, positioned column 4 , line 2 is M . The letter in grid 2, positioned column 3 , line 5 is O . M and O are therefore the 2 encrypted letters.

Repeat the 4 operations for each bigram , and repeat the complete algorithm for each block of 6 letters of plain text.

Example: The other 2 triplets give LG and AZ , the final encrypted message is: MOLGAZ

## How to decrypt Digrafid cipher?

Decryption is identical to the encryption process.

## How to recognize a Digrafid ciphertext?

The encrypted message has a fairly low index of coincidence . The message has no specific characteristics, a hacker can attack it by a frequency analysis of bigrams .

## What are the variants of the Digrafid cipher?

Multiple variants can be created (and it can be written Digrafide ). First, the reading order of the grids may be reversed (both at the beginning step and the end step). Then, the order of triplet numbers can be changed by transposition . Finally, the grid sizes can be changed, even if 3 * 9 = 27 is very convenient.
