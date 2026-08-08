# Four Square Cipher

> Source: [https://www.dcode.fr/four-squares-cipher](https://www.dcode.fr/four-squares-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## How to encrypt using Four Squares cipher?

The 4-squares encryption is made, as its name suggests, with four square grids (possibly generated from a keyword) themselves positioned in a square:

Grid 1 Grid 2 Grid 3 Grid 4

Grid 1 Grid 2 Grid 3 Grid 4

Example: 4 grids formed from the first names JOHN , GEORGE , PAUL and RINGO (the letter Z is omitted) \ 1 2 3 4 5 1 J O H N A 2 B C D E F 3 G I K L M 4 P Q R S T 5 U V W X Y \ 1 2 3 4 5 1 G E O R A 2 B C D F H 3 I J K L M 4 N P Q S T 5 U V W X Y \ 1 2 3 4 5 1 P A U L B 2 C D E F G 3 H I J K M 4 N O Q R S 5 T V W X Y \ 1 2 3 4 5 1 R I N G O 2 A B C D E 3 F H J K L 4 M P Q S T 5 U V W X Y

\ 1 2 3 4 5 1 J O H N A 2 B C D E F 3 G I K L M 4 P Q R S T 5 U V W X Y \ 1 2 3 4 5 1 G E O R A 2 B C D F H 3 I J K L M 4 N P Q S T 5 U V W X Y \ 1 2 3 4 5 1 P A U L B 2 C D E F G 3 H I J K M 4 N O Q R S 5 T V W X Y \ 1 2 3 4 5 1 R I N G O 2 A B C D E 3 F H J K L 4 M P Q S T 5 U V W X Y

\ 1 2 3 4 5 1 J O H N A 2 B C D E F 3 G I K L M 4 P Q R S T 5 U V W X Y

\ 1 2 3 4 5 1 G E O R A 2 B C D F H 3 I J K L M 4 N P Q S T 5 U V W X Y

\ 1 2 3 4 5 1 P A U L B 2 C D E F G 3 H I J K M 4 N O Q R S 5 T V W X Y

\ 1 2 3 4 5 1 R I N G O 2 A B C D E 3 F H J K L 4 M P Q S T 5 U V W X Y

The first step is to split the plain message into pairs of two letters (completed with a neutral letter if necessary).

Example: The plain message BEATLES is decomposed into 'BE, AT, LE, SX'

For each pair ( bigram ), locate the first letter in grid 1 and the second letter in grid 4. Intersect the rows and columns of the letters found in the two adjacent grids and write down these 2 new letters.

Example: Bigramme BE : B is positioned (row 2, column 1) in grid 1 E is positioned (row 2, column 5) in grid 4 The extension of their rows and Columns in grids 2 and 3 leads to 2 intersections: H , positioned (row 2, column 5) in grid 2 and C , positioned (row 2, column 1) in grid 3 \ 1 2 3 4 5 1 J O H N A 2 B → → → → 3 ↓ I K L M 4 ↓ Q R S T 5 ↓ V W X Y \ 1 2 3 4 5 1 G E O R A 2 → → → → H 3 I J K L ↑ 4 N P Q S ↑ 5 U V W X ↑ \ 1 2 3 4 5 1 ↓ A U L B 2 C ← ← ← ← 3 H I J K M 4 N O Q R S 5 T V W X Y \ 1 2 3 4 5 1 R I N G ↑ 2 ← ← ← ← E 3 F H J K L 4 M P Q S T 5 U V W X Y

\ 1 2 3 4 5 1 J O H N A 2 B → → → → 3 ↓ I K L M 4 ↓ Q R S T 5 ↓ V W X Y \ 1 2 3 4 5 1 G E O R A 2 → → → → H 3 I J K L ↑ 4 N P Q S ↑ 5 U V W X ↑ \ 1 2 3 4 5 1 ↓ A U L B 2 C ← ← ← ← 3 H I J K M 4 N O Q R S 5 T V W X Y \ 1 2 3 4 5 1 R I N G ↑ 2 ← ← ← ← E 3 F H J K L 4 M P Q S T 5 U V W X Y

\ 1 2 3 4 5 1 J O H N A 2 B → → → → 3 ↓ I K L M 4 ↓ Q R S T 5 ↓ V W X Y

\ 1 2 3 4 5 1 G E O R A 2 → → → → H 3 I J K L ↑ 4 N P Q S ↑ 5 U V W X ↑

\ 1 2 3 4 5 1 ↓ A U L B 2 C ← ← ← ← 3 H I J K M 4 N O Q R S 5 T V W X Y

\ 1 2 3 4 5 1 R I N G ↑ 2 ← ← ← ← E 3 F H J K L 4 M P Q S T 5 U V W X Y

The encrypted text consists of the letters found at the intersections: first the letter in the grid 2 and then the letter in the grid 3.

Example: The final encrypted message is HCASMFSX

## How to decrypt Four Squares cipher?

4 Squares decryption is almost identical to the encryption. The difference is that it is necessary to position the letters of the encrypted bigram in grids 2 and 3, then read the light letters in grids 1 and 4.

Example: (See above) the bigramme HC is positioned in grids 2 and 3 and deciphers BE in grids 1 and 4. \ 1 2 3 4 5 1 J O H N A 2 B ← ← ← ← 3 ↑ I K L M 4 ↑ Q R S T 5 ↑ V W X Y \ 1 2 3 4 5 1 G E O R A 2 ← ← ← ← H 3 I J K L ↓ 4 N P Q S ↓ 5 U V W X ↓ \ 1 2 3 4 5 1 ↑ A U L B 2 C → → → → 3 H I J K M 4 N O Q R S 5 T V W X Y \ 1 2 3 4 5 1 R I N G ↓ 2 → → → → E 3 F H J K L 4 M P Q S T 5 U V W X Y The message HCASMFSX is decrypted BEATLESX

\ 1 2 3 4 5 1 J O H N A 2 B ← ← ← ← 3 ↑ I K L M 4 ↑ Q R S T 5 ↑ V W X Y \ 1 2 3 4 5 1 G E O R A 2 ← ← ← ← H 3 I J K L ↓ 4 N P Q S ↓ 5 U V W X ↓ \ 1 2 3 4 5 1 ↑ A U L B 2 C → → → → 3 H I J K M 4 N O Q R S 5 T V W X Y \ 1 2 3 4 5 1 R I N G ↓ 2 → → → → E 3 F H J K L 4 M P Q S T 5 U V W X Y

\ 1 2 3 4 5 1 J O H N A 2 B ← ← ← ← 3 ↑ I K L M 4 ↑ Q R S T 5 ↑ V W X Y

\ 1 2 3 4 5 1 G E O R A 2 ← ← ← ← H 3 I J K L ↓ 4 N P Q S ↓ 5 U V W X ↓

\ 1 2 3 4 5 1 ↑ A U L B 2 C → → → → 3 H I J K M 4 N O Q R S 5 T V W X Y

\ 1 2 3 4 5 1 R I N G ↓ 2 → → → → E 3 F H J K L 4 M P Q S T 5 U V W X Y

## How to recognize a 4 Squares ciphertext?

Four Squares is a polygrammic encryption, so it is advisable to perform an analysis of the bigrams if the text is long enough.

Also, the presence of 4 keywords that can generate the grids is a clue.

Grids with 25 letters, there is normally at least one missing letter from Latin alphabet in the encrypted text.

The company foursquare has a name that can be linked with this cipher.

## What are the variants of the 4-Squares cipher?

Variation 1: reverse the order of the bigram obtained. Rather than taking the encrypted letters in the grid 2 then the grid 3, it is possible to reverse this bigram and take the grid 3 then the grid 2.

Option 2: Switch the position of grids 1, 2, 3 and 4.
