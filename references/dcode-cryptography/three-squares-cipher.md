# Three Squares Cipher

> Source: [https://www.dcode.fr/three-squares-cipher](https://www.dcode.fr/three-squares-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is the Three Squares cipher? (Definition)

The 3-square cipher is a polygrammic cipher using 3 grids. From plain text bigrams , it generates ciphered trigrams according to the position of the letters in the three grids.

## How to encrypt using Three Squares cipher?

3-square encryption is done with three grids (possibly generated from a keyword or disordered alphabet )

Example: Encrypt MESSAGE with the keys ONE , TWO , THREE corresponding to the grids (2) \ 1 2 3 4 5 1 T W O A B 2 C D E F G 3 H I J K L 4 M N P Q R 5 S U V X Y \ 1 2 3 4 5 1 O N E A B 2 C D F G H 3 I J K L M 4 P Q R S T 5 U V W X Y (1) \ 1 2 3 4 5 1 T H R E A 2 B C D F G 3 I J K L M 4 N O P Q S 5 U V W X Y (3)

(2) \ 1 2 3 4 5 1 T W O A B 2 C D E F G 3 H I J K L 4 M N P Q R 5 S U V X Y \ 1 2 3 4 5 1 O N E A B 2 C D F G H 3 I J K L M 4 P Q R S T 5 U V W X Y (1) \ 1 2 3 4 5 1 T H R E A 2 B C D F G 3 I J K L M 4 N O P Q S 5 U V W X Y (3)

\ 1 2 3 4 5 1 T W O A B 2 C D E F G 3 H I J K L 4 M N P Q R 5 S U V X Y

\ 1 2 3 4 5 1 O N E A B 2 C D F G H 3 I J K L M 4 P Q R S T 5 U V W X Y

\ 1 2 3 4 5 1 T H R E A 2 B C D F G 3 I J K L M 4 N O P Q S 5 U V W X Y

Split the plain message into bigrams (pairs of two letters respectively noted L1 and L2 ). Complete with a neutral letter of the second grid if the message has an odd length.

Find L1 in grid 1 and L2 in grid 2. Then note the intersection in grid 3 of the row of L1 in grid 1 with the column of L2 in the grid 2 .

Example: For the bigram ME , M is in position (row 3 , column 5 ) in grid 1 , and E is in position (row 2 , column 3 ) in the grid 2 . The intersection in grid 3 is the letter K (row 3 , column 3 ).

Each bigram of the plain text is associated with 3 new letters: a letter taken randomly in the same column as the letter in the grid 1 , the letter intersection of the grid 3 and a letter taken randomly in the same row as the letter of the grid 2 . These 3 letters (a trigram ) represent the coded text for the bigram .

Example: Take T : a random letter in the column 5 ( BHMTY ) of the grid 1 Take K : the intersection letter of the grid 3 previously found Take ' D ': a random letter in the row 2 ( CDEFG ) of the grid 2 The corresponding encrypted trigram is TKD . Repeat the process for each bigram . The final encrypted message is TKDGNVSAFRAV .

## How to decrypt Three Squares cipher?

Decryption by three squares is done with three grids.

Example: Decrypt UDBJDC with the keys ONE , TWO , THREE' corresponding to the grids (2) \ 1 2 3 4 5 1 T W O A B 2 C D E F G 3 H I J K L 4 M N P Q R 5 S U V X Y \ 1 2 3 4 5 1 O N E A B 2 C D F G H 3 I J K L M 4 P Q R S T 5 U V W X Y (1) \ 1 2 3 4 5 1 T H R E A 2 B C D F G 3 I J K L M 4 N O P Q S 5 U V W X Y (3)

(2) \ 1 2 3 4 5 1 T W O A B 2 C D E F G 3 H I J K L 4 M N P Q R 5 S U V X Y \ 1 2 3 4 5 1 O N E A B 2 C D F G H 3 I J K L M 4 P Q R S T 5 U V W X Y (1) \ 1 2 3 4 5 1 T H R E A 2 B C D F G 3 I J K L M 4 N O P Q S 5 U V W X Y (3)

\ 1 2 3 4 5 1 T W O A B 2 C D E F G 3 H I J K L 4 M N P Q R 5 S U V X Y

\ 1 2 3 4 5 1 O N E A B 2 C D F G H 3 I J K L M 4 P Q R S T 5 U V W X Y

\ 1 2 3 4 5 1 T H R E A 2 B C D F G 3 I J K L M 4 N O P Q S 5 U V W X Y

Split the message into trigrams (triplets of three letters L1 , L2 and L3 ) and find L1 in the grid 1 , L2 in the grid 3 and L3 in the grid 2 .

Example: The first trigram is UDB , U is in position (row 5 , column 1 ) in grid 1 , D is in position (row 2 , column 3 ) in grid 3 , and B is in position (row 1 , column 5 ) in grid 2.

Find the 2 plain letters: Plain letter 1: intersection of the row of the letter L2 in the grid 3 with the column of the letter L1 in the grid 1 Plain letter 2: intersection of the letter L2 column in grid 3 with the row of the letter L3 in grid 2 .

Example: The first plain letter is C , intersection of row 2 of D in grid 3 with column 1 of U in grid 1 . The second plain letter is O , intersection of column 3 of D in grid 3 with row 1 of B in grid 2 . Finally the complete plain message is CODE .

## How to recognize a 3 squares ciphertext?

The message has a length multiple of 3 .

The final ciphertext is longer than the original of 33%.

The frequency analysis and the coincidence index is similar to an almost random text.

The text is theoretically composed of a maximum of 25 distinct characters if the grids are 5x5 and use the same letters of the alphabet.

## What are the variants of the Three Squares cipher?

In the three-square cipher , several ways of ciphering and noting the letters are possible:

The first letter of the bigram is sought in grid 1 and the second letter in grid 2, noted 1-2 (by default) but it is possible to reverse, notation 2-1 .

The trigram is then generally noted as follows: - a letter taken randomly from the same column as the letter in grid 1 - the letter from grid 3 - a letter taken randomly from the same row as the letter of the grid 2 This cipher is indicated 1-3-2 (by default). It is also possible to encrypt with a different order.

Finally, it is possible to mix the grids, such as inverting grids 1 and 2, or other permutation.
